"""YANA unit test suite — 20 tests covering security, platform mapping,
SSH transport, tool integration, inventory, status, intent, ingest, and RAG."""
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import ValidationError

from input_models.models import (
    DeviceListQuery, IntentQuery, KBQuery,
    OspfQuery, RoutingQuery, TracerouteInput,
)
from platforms.platform_map import PLATFORM_MAP, _apply_vrf
from tools.intent import query_intent
from tools.inventory_tool import list_devices
from tools.operational import traceroute
from tools.ospf import get_ospf
from tools.routing import get_routing
from tools.status import get_status
from transport.ssh import _build_cli, execute_ssh

import core.inventory as _inv
_real_get_device = _inv.get_device

CHROMA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "chroma"


# ── Security ─────────────────────────────────────────────────────────────────

_INJECTION_PATTERNS = [
    "$(reboot)", "`reboot`", "VRF1|cat /etc/shadow",
    "VRF1\nshow running-config", "VRF1\x00cmd", "VRF1 extra",
    "VRF1&& rm -rf /", "VRF1>/tmp/x", "VRF1'", 'VRF1"',
    "${PATH}", "", "   ", "VRF1\uff1b", "VRF1\u2223",
    "VRF1;cmd", "VRF1\tval", "A" * 33,
]

_VALID_VRFS = ["VRF1", "my_vrf", "prod-vrf", "A" * 32, "V", "VRF_123-abc"]


@pytest.mark.parametrize("bad_vrf", _INJECTION_PATTERNS)
def test_vrf_injection_blocked(bad_vrf):
    with pytest.raises(ValidationError):
        OspfQuery(device="R1", query="neighbors", vrf=bad_vrf)


@pytest.mark.parametrize("good_vrf", _VALID_VRFS)
def test_vrf_valid_names_accepted(good_vrf):
    q = OspfQuery(device="R1", query="neighbors", vrf=good_vrf)
    assert q.vrf == good_vrf


# ── Platform map ─────────────────────────────────────────────────────────────

EXPECTED_CLI_STYLES = {"ios", "eos", "junos", "aos", "routeros", "vyos"}
OSPF_QUERIES = {"neighbors", "database", "borders", "config", "interfaces", "details"}
ROUTING_QUERIES = {"ip_route", "route_maps", "prefix_lists", "policy_based_routing", "access_lists"}


def test_all_vendors_present():
    assert set(PLATFORM_MAP.keys()) == EXPECTED_CLI_STYLES


def test_all_query_types_complete():
    for style in EXPECTED_CLI_STYLES:
        assert set(PLATFORM_MAP[style]["ospf"].keys()) == OSPF_QUERIES
        assert set(PLATFORM_MAP[style]["routing_table"].keys()) == ROUTING_QUERIES
        assert "interface_status" in PLATFORM_MAP[style]["interfaces"]
        assert "traceroute" in PLATFORM_MAP[style]["tools"]


def test_vrf_dict_routing():
    action = {"default": "show ip route", "vrf": "show ip route vrf {vrf}"}
    assert _apply_vrf(action, "VRF1") == "show ip route vrf VRF1"
    assert _apply_vrf(action, None) == "show ip route"


def test_vrf_default_treated_as_no_vrf():
    action = {"default": "show ip ospf neighbor", "vrf": "show ip ospf neighbor vrf {vrf}"}
    assert _apply_vrf(action, "default") == "show ip ospf neighbor"
    assert _apply_vrf(action, "DEFAULT") == "show ip ospf neighbor"


# ── SSH transport ────────────────────────────────────────────────────────────

MIKROTIK_DEVICE = {"host": "10.0.0.5", "platform": "mikrotik_routeros", "cli_style": "routeros"}
IOS_DEVICE = {"host": "10.0.0.1", "platform": "cisco_iosxe", "cli_style": "ios"}


def _async_cm(raw_result):
    mock_conn = AsyncMock()
    mock_conn.send_input_async.return_value = MagicMock(result=raw_result)
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=mock_conn)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


def _failing_cm(exc):
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(side_effect=exc)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


def test_mikrotik_username_ct_suffix():
    with patch("transport.ssh.USERNAME", "admin"), \
         patch("transport.ssh.PASSWORD", "pass"), \
         patch("transport.ssh.Cli") as mock_cli, \
         patch("transport.ssh.BinOptions"):
        _build_cli(MIKROTIK_DEVICE)
    assert mock_cli.call_args.kwargs["auth_options"].username == "admin+ct"


async def test_open_exception_no_retry():
    from scrapli.exceptions import OpenException
    call_count = 0

    def counting_build(*a, **kw):
        nonlocal call_count
        call_count += 1
        return _failing_cm(OpenException("refused"))

    with patch("transport.ssh._build_cli", side_effect=counting_build), \
         patch("transport.ssh.SSH_RETRIES", 1):
        with pytest.raises(OpenException):
            await execute_ssh(IOS_DEVICE, "show version")
    assert call_count == 1


async def test_transient_error_retries_and_recovers():
    attempt = 0

    def flaky_build(*a, **kw):
        nonlocal attempt
        attempt += 1
        if attempt == 1:
            return _failing_cm(ConnectionError("transient"))
        return _async_cm("recovered output")

    with patch("transport.ssh._build_cli", side_effect=flaky_build), \
         patch("transport.ssh.SSH_RETRIES", 1), \
         patch("transport.ssh.SSH_RETRY_DELAY", 0):
        result = await execute_ssh(IOS_DEVICE, "show version")
    assert result == "recovered output"


# ── Tool integration ─────────────────────────────────────────────────────────

async def test_unknown_device_error():
    result = await get_ospf(OspfQuery(device="NONEXISTENT", query="neighbors"))
    assert "error" in result
    assert "Unknown device" in result["error"]


async def test_ospf_full_stack_ios():
    with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
        mock_ssh.return_value = "Neighbor ID  State\n1.1.1.1  FULL"
        result = await get_ospf(OspfQuery(device="R1", query="neighbors"))
    assert result["device"] == "R1"
    assert result["cli_style"] == "ios"
    assert "show ip ospf neighbor" in result["_command"]


async def test_vrf_flows_to_command():
    with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
        mock_ssh.return_value = "mock output"
        result = await get_ospf(OspfQuery(device="R2", query="neighbors", vrf="VRF2"))
    assert "vrf VRF2" in result["_command"]
    assert "VRF1" not in result["_command"]


async def test_traceroute_source_appended():
    with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
        mock_ssh.return_value = "1  10.0.0.254  1 ms"
        result = await traceroute(TracerouteInput(device="R1", destination="10.0.0.1", source="192.168.1.1"))
    assert "source 192.168.1.1" in result["_command"]


async def test_routing_full_stack_ios():
    with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
        mock_ssh.return_value = "O    10.0.0.0/24 [110/20] via 10.0.0.1"
        result = await get_routing(RoutingQuery(device="R1", query="ip_route"))
    assert result["device"] == "R1"
    assert result["cli_style"] == "ios"
    assert result["_command"] == "show ip route vrf VRF1"


# ── Inventory & device listing ───────────────────────────────────────────────

def test_device_lookup_returns_dict(monkeypatch):
    monkeypatch.setattr(_inv, "get_device", _real_get_device)
    result = _inv.get_device("R1")
    assert result["cli_style"] == "ios"
    assert result["host"] == "10.0.0.1"


async def test_filter_by_cli_style():
    result = await list_devices(DeviceListQuery(cli_style="eos"))
    assert list(result["devices"].keys()) == ["R2"]
    assert result["devices"]["R2"]["cli_style"] == "eos"


# ── Status & intent ──────────────────────────────────────────────────────────

async def test_status_structure():
    with patch("tools.status._CHROMA_DIR") as mc, \
         patch("tools.status._INTENT_JSON") as mi:
        mc.exists.return_value = False
        mi.exists.return_value = False
        result = await get_status()
    assert set(result.keys()) == {"inventory", "intent", "chromadb"}
    assert result["inventory"]["device_count"] == 6
    assert result["inventory"]["source"] == "network_json"
    assert result["intent"]["source"] == "unavailable"
    assert result["chromadb"]["available"] is False


async def test_intent_single_device_filter(tmp_path):
    intent = {"routers": {"R1": {"roles": ["ABR"]}, "R2": {"roles": ["ASBR"]}}}
    intent_file = tmp_path / "INTENT.json"
    intent_file.write_text(json.dumps(intent))

    with patch("tools.intent._INTENT_JSON", intent_file):
        result = await query_intent(IntentQuery(device="R1"))
    assert result["device"] == "R1"
    assert result["intent"]["roles"] == ["ABR"]


# ── Ingest ───────────────────────────────────────────────────────────────────

def test_vendor_file_metadata():
    from ingest import extract_metadata
    meta = extract_metadata(Path("docs/vendor_cisco_ios.md"))
    assert meta["vendor"] == "cisco_ios"
    assert meta["topic"] == "vendor_guide"
    assert meta["protocol"] == "ospf"


# ── RAG pipeline (requires ChromaDB) ────────────────────────────────────────

@pytest.mark.skipif(not CHROMA_DIR.exists(), reason="ChromaDB not populated")
async def test_kb_basic_query():
    from tools.rag import search_knowledge_base
    result = await search_knowledge_base(KBQuery(query="OSPF neighbor states"))
    assert len(result["results"]) > 0
    for r in result["results"]:
        assert "content" in r
        assert "metadata" in r


# ── Adversarial input ────────────────────────────────────────────────────────

_BAD_DEVICES = [
    "; rm -rf /", "' OR 1=1 --", "a" * 65, "",
    "R1 extra", "R1\nshow run", "R1;cmd", "$(reboot)",
    "R1\x00cmd", "R1&& cat /etc/shadow",
]

_VALID_DEVICES = ["R1", "my_device", "core-rtr_01", "A" * 64]


@pytest.mark.parametrize("bad_device", _BAD_DEVICES)
def test_adversarial_device_name_blocked(bad_device):
    with pytest.raises(ValidationError):
        OspfQuery(device=bad_device, query="neighbors")


@pytest.mark.parametrize("good_device", _VALID_DEVICES)
def test_valid_device_names_accepted(good_device):
    q = OspfQuery(device=good_device, query="neighbors")
    assert q.device == good_device
