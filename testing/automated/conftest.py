"""Conftest for automated tests — stubs transport, vault, netbox to prevent live connections."""
import sys
from pathlib import Path

import pytest

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Mock devices — one per cli_style
MOCK_DEVICES = {
    "R1": {"host": "10.0.0.1", "platform": "cisco_iosxe", "cli_style": "ios", "vrf": "VRF1"},
    "R2": {"host": "10.0.0.2", "platform": "arista_eos", "cli_style": "eos", "vrf": "VRF1"},
    "R3": {"host": "10.0.0.3", "platform": "juniper_junos", "cli_style": "junos", "vrf": "VRF1"},
    "R4": {"host": "10.0.0.4", "platform": "aruba_aoscx", "cli_style": "aos"},
    "R5": {"host": "10.0.0.5", "platform": "mikrotik_routeros", "cli_style": "routeros"},
    "R6": {"host": "10.0.0.6", "platform": "vyos_vyos", "cli_style": "vyos"},
}


def _mock_get_device(name):
    if name not in MOCK_DEVICES:
        known = ", ".join(sorted(MOCK_DEVICES))
        raise KeyError(f"Unknown device {name!r} — known: {known}")
    return MOCK_DEVICES[name]


@pytest.fixture(autouse=True)
def mock_inventory(monkeypatch):
    """Replace the devices dict and get_device everywhere they're imported."""
    import core.inventory
    import tools.ospf
    import tools.operational
    import tools.routing
    import tools.inventory_tool
    import transport

    monkeypatch.setattr(core.inventory, "devices", MOCK_DEVICES)
    monkeypatch.setattr(core.inventory, "source", "netbox")
    monkeypatch.setattr(core.inventory, "get_device", _mock_get_device)
    monkeypatch.setattr(tools.ospf, "get_device", _mock_get_device)
    monkeypatch.setattr(tools.operational, "get_device", _mock_get_device)
    monkeypatch.setattr(tools.routing, "get_device", _mock_get_device)
    monkeypatch.setattr(tools.inventory_tool, "devices", MOCK_DEVICES)
    monkeypatch.setattr(transport, "get_device", _mock_get_device)
