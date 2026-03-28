"""UT-003: Tool layer — get_ospf, get_interfaces, traceroute, _error_response, and VRF integration."""
from unittest.mock import AsyncMock, patch

import pytest

from input_models.models import InterfacesQuery, OspfQuery, TracerouteInput
from tools import _error_response
from tools.operational import get_interfaces, traceroute
from tools.ospf import get_ospf


class TestErrorResponse:
    def test_with_device(self):
        r = _error_response("R1", "something failed")
        assert r == {"error": "something failed", "device": "R1"}

    def test_without_device(self):
        r = _error_response(None, "something failed")
        assert r == {"error": "something failed"}
        assert "device" not in r


class TestGetOspf:
    async def test_unknown_device(self):
        result = await get_ospf(OspfQuery(device="NONEXISTENT", query="neighbors"))
        assert "error" in result
        assert "Unknown device" in result["error"]

    async def test_valid_device_ios(self):
        """Full-stack: command resolves correctly, transport dict built from real inventory."""
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "Neighbor ID  State\n1.1.1.1  FULL"
            result = await get_ospf(OspfQuery(device="R1", query="neighbors"))
        assert result["device"] == "R1"
        assert result["cli_style"] == "ios"   # from MOCK_DEVICES["R1"], not mock-hardcoded
        assert "show ip ospf neighbor" in result["_command"]
        assert "FULL" in result["raw"]

    async def test_valid_device_eos(self):
        """cli_style is read from the device dict — verified by checking a second vendor."""
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "mock eos output"
            result = await get_ospf(OspfQuery(device="R2", query="neighbors"))
        assert result["cli_style"] == "eos"   # R2 is eos in MOCK_DEVICES

    async def test_vrf_passed_through(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "mock output"
            result = await get_ospf(OspfQuery(device="R2", query="neighbors", vrf="VRF1"))
        assert "VRF1" in result["_command"]


class TestGetInterfaces:
    async def test_unknown_device(self):
        result = await get_interfaces(InterfacesQuery(device="NONEXISTENT"))
        assert "error" in result
        assert "Unknown device" in result["error"]

    async def test_valid_device_ios(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "GigabitEthernet0/0  up  up  10.0.0.1"
            result = await get_interfaces(InterfacesQuery(device="R1"))
        assert result["device"] == "R1"
        assert result["cli_style"] == "ios"   # from MOCK_DEVICES["R1"], not mock-hardcoded
        assert "raw" in result

    async def test_valid_device_junos(self):
        """cli_style comes from the device dict — verified with a third vendor."""
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "ge-0/0/0  up  up"
            result = await get_interfaces(InterfacesQuery(device="R3"))
        assert result["cli_style"] == "junos"  # R3 is junos in MOCK_DEVICES


class TestTraceroute:
    async def test_unknown_device(self):
        result = await traceroute(TracerouteInput(device="NONEXISTENT", destination="10.0.0.1"))
        assert "error" in result
        assert "Unknown device" in result["error"]

    async def test_valid_device_ios_basic(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "1  10.0.0.254  1 ms"
            result = await traceroute(TracerouteInput(device="R1", destination="10.0.0.1"))
        assert result["device"] == "R1"
        assert result["cli_style"] == "ios"
        assert "traceroute" in result["_command"]
        assert "10.0.0.1" in result["_command"]

    async def test_ios_source_appended(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "1  10.0.0.254  1 ms"
            result = await traceroute(TracerouteInput(device="R1", destination="10.0.0.1", source="192.168.1.1"))
        assert "source 192.168.1.1" in result["_command"]

    async def test_eos_vrf_in_command(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "mock output"
            result = await traceroute(TracerouteInput(device="R2", destination="10.0.0.1", vrf="VRF2"))
        assert "vrf VRF2" in result["_command"]
        assert "10.0.0.1" in result["_command"]

    async def test_routeros_address_syntax(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "mock output"
            result = await traceroute(TracerouteInput(device="R5", destination="10.0.0.1"))
        assert "address=10.0.0.1" in result["_command"]

    async def test_routeros_source_syntax(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "mock output"
            result = await traceroute(TracerouteInput(device="R5", destination="10.0.0.1", source="192.168.1.1"))
        assert "address=10.0.0.1" in result["_command"]
        assert "src-address=192.168.1.1" in result["_command"]


class TestVrfEndToEnd:
    async def test_explicit_vrf_in_final_command(self):
        """VRF flows from validated input → get_action substitution → final CLI command."""
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "mock output"
            # R2 is eos; explicit vrf="VRF2" should override R2's device vrf="VRF1"
            result = await get_ospf(OspfQuery(device="R2", query="neighbors", vrf="VRF2"))
        assert "vrf VRF2" in result["_command"]
        assert "VRF1" not in result["_command"]


class TestAdversarialDeviceName:
    @pytest.mark.parametrize("bad_device", [
        "; rm -rf /",
        "' OR 1=1 --",
        "a" * 1000,
        "",
    ])
    async def test_adversarial_name_returns_clean_error(self, bad_device):
        """Adversarial device names hit inventory lookup, not shell/DB — clean error returned."""
        result = await get_ospf(OspfQuery(device=bad_device, query="neighbors"))
        assert "error" in result
        # No exception raised, no command executed
