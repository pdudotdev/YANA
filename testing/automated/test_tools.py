"""UT-003: Tool layer — tests get_ospf and get_interfaces with mocked transport."""
import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from input_models.models import InterfacesQuery, OspfQuery
from tools.ospf import get_ospf
from tools.operational import get_interfaces

MOCK_RESULT = {
    "device": "R1",
    "_command": "show ip ospf neighbor",
    "cli_style": "ios",
    "raw": "Neighbor ID  State\n1.1.1.1  FULL",
}


def _make_mock(command_override=None):
    async def _fake(device_name, action):
        return {
            "device": device_name,
            "_command": action,
            "cli_style": "ios",
            "raw": f"mock output for {action}",
        }
    return _fake


class TestGetOspf:
    def test_unknown_device(self):
        result = asyncio.get_event_loop().run_until_complete(
            get_ospf(OspfQuery(device="NONEXISTENT", query="neighbors"))
        )
        assert "error" in result
        assert "Unknown device" in result["error"]

    def test_valid_device_returns_result(self):
        with patch("tools.ospf.execute_command", new=_make_mock()):
            result = asyncio.get_event_loop().run_until_complete(
                get_ospf(OspfQuery(device="R1", query="neighbors"))
            )
        assert result["device"] == "R1"
        assert result["cli_style"] == "ios"
        assert "_command" in result
        assert "raw" in result
        assert "show ip ospf neighbor" in result["_command"]

    def test_vrf_passed_through(self):
        with patch("tools.ospf.execute_command", new=_make_mock()):
            result = asyncio.get_event_loop().run_until_complete(
                get_ospf(OspfQuery(device="R2", query="neighbors", vrf="VRF1"))
            )
        assert "VRF1" in result["_command"]


class TestGetInterfaces:
    def test_unknown_device(self):
        result = asyncio.get_event_loop().run_until_complete(
            get_interfaces(InterfacesQuery(device="NONEXISTENT"))
        )
        assert "error" in result
        assert "Unknown device" in result["error"]

    def test_valid_device_returns_result(self):
        with patch("tools.operational.execute_command", new=_make_mock()):
            result = asyncio.get_event_loop().run_until_complete(
                get_interfaces(InterfacesQuery(device="R1"))
            )
        assert result["device"] == "R1"
        assert result["cli_style"] == "ios"
        assert "raw" in result
