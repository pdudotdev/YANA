"""UT-010: get_routing tool."""
from unittest.mock import AsyncMock, patch

import pytest

from input_models.models import RoutingQuery
from tools.routing import get_routing


class TestGetRouting:
    async def test_unknown_device(self):
        result = await get_routing(RoutingQuery(device="NONEXISTENT", query="ip_route"))
        assert "error" in result
        assert "Unknown device" in result["error"]

    async def test_valid_device_ios(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "S    0.0.0.0/0 via 10.0.0.254"
            result = await get_routing(RoutingQuery(device="R1", query="ip_route"))
        assert result["device"] == "R1"
        assert result["cli_style"] == "ios"
        assert "show ip route" in result["_command"]

    async def test_valid_device_eos(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "mock eos route output"
            result = await get_routing(RoutingQuery(device="R2", query="ip_route"))
        assert result["cli_style"] == "eos"

    async def test_vrf_in_command(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "mock output"
            result = await get_routing(RoutingQuery(device="R2", query="ip_route", vrf="VRF1"))
        assert "VRF1" in result["_command"]

    async def test_route_maps_query(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "route-map RM_OUT permit 10"
            result = await get_routing(RoutingQuery(device="R1", query="route_maps"))
        assert result["device"] == "R1"

    @pytest.mark.parametrize("query", ["ip_route", "route_maps", "prefix_lists", "policy_based_routing", "access_lists"])
    async def test_all_query_types_resolve(self, query):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "mock output"
            result = await get_routing(RoutingQuery(device="R1", query=query))
        assert "error" not in result
