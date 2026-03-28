"""UT-002: Platform map structure and VRF resolution."""
import pytest

from platforms.platform_map import PLATFORM_MAP, _apply_vrf, get_action

EXPECTED_CLI_STYLES = {"ios", "eos", "junos", "aos", "routeros", "vyos"}
OSPF_QUERIES = {"neighbors", "database", "borders", "config", "interfaces", "details"}
ROUTING_QUERIES = {"ip_route", "route_maps", "prefix_lists", "policy_based_routing", "access_lists"}


class TestPlatformMapStructure:
    def test_all_vendors_present(self):
        assert set(PLATFORM_MAP.keys()) == EXPECTED_CLI_STYLES

    @pytest.mark.parametrize("cli_style", EXPECTED_CLI_STYLES)
    def test_ospf_queries_complete(self, cli_style):
        ospf = PLATFORM_MAP[cli_style]["ospf"]
        assert set(ospf.keys()) == OSPF_QUERIES, f"{cli_style} missing OSPF queries"

    @pytest.mark.parametrize("cli_style", EXPECTED_CLI_STYLES)
    def test_routing_queries_complete(self, cli_style):
        routing = PLATFORM_MAP[cli_style]["routing_table"]
        assert set(routing.keys()) == ROUTING_QUERIES, f"{cli_style} missing routing queries"

    @pytest.mark.parametrize("cli_style", EXPECTED_CLI_STYLES)
    def test_interfaces_present(self, cli_style):
        assert "interface_status" in PLATFORM_MAP[cli_style]["interfaces"]

    @pytest.mark.parametrize("cli_style", EXPECTED_CLI_STYLES)
    def test_traceroute_present(self, cli_style):
        assert "traceroute" in PLATFORM_MAP[cli_style]["tools"], f"{cli_style} missing traceroute"


class TestApplyVrf:
    def test_dict_with_vrf(self):
        action = {"default": "show ip ospf neighbor", "vrf": "show ip ospf neighbor vrf {vrf}"}
        result = _apply_vrf(action, "VRF1")
        assert result == "show ip ospf neighbor vrf VRF1"

    def test_dict_without_vrf(self):
        action = {"default": "show ip ospf neighbor", "vrf": "show ip ospf neighbor vrf {vrf}"}
        result = _apply_vrf(action, None)
        assert result == "show ip ospf neighbor"

    def test_plain_string_no_placeholder(self):
        result = _apply_vrf("show ip ospf neighbor", "VRF1")
        assert result == "show ip ospf neighbor"

    def test_plain_string_with_placeholder(self):
        result = _apply_vrf("show ip ospf neighbor vrf {vrf}", "VRF1")
        assert result == "show ip ospf neighbor vrf VRF1"

    def test_plain_string_none_vrf(self):
        result = _apply_vrf("show ip ospf neighbor", None)
        assert result == "show ip ospf neighbor"

    def test_default_vrf_treated_as_no_vrf(self):
        """'default' VRF name must use the default (non-VRF) command variant."""
        action = {"default": "show ip ospf neighbor", "vrf": "show ip ospf neighbor vrf {vrf}"}
        result = _apply_vrf(action, "default")
        assert result == "show ip ospf neighbor"

    def test_default_vrf_case_insensitive(self):
        action = {"default": "show ip ospf neighbor", "vrf": "show ip ospf neighbor vrf {vrf}"}
        assert _apply_vrf(action, "DEFAULT") == "show ip ospf neighbor"
        assert _apply_vrf(action, "Default") == "show ip ospf neighbor"


class TestRoutingTableVrf:
    def test_eos_ip_route_with_vrf(self):
        device = {"cli_style": "eos"}
        result = get_action(device, "routing_table", "ip_route", vrf="VRF1")
        assert result == "show ip route vrf VRF1"

    def test_eos_ip_route_no_vrf(self):
        device = {"cli_style": "eos"}
        result = get_action(device, "routing_table", "ip_route")
        assert result == "show ip route"

    def test_junos_ip_route_with_vrf(self):
        device = {"cli_style": "junos"}
        result = get_action(device, "routing_table", "ip_route", vrf="VRF1")
        assert result == "show route instance VRF1"

    def test_ios_ip_route_no_vrf_variant(self):
        device = {"cli_style": "ios"}
        result = get_action(device, "routing_table", "ip_route")
        assert result == "show ip route"

    def test_routeros_ip_route(self):
        device = {"cli_style": "routeros"}
        result = get_action(device, "routing_table", "ip_route")
        assert result == "/ip route print without-paging"


class TestTracerouteVrf:
    def test_ios_traceroute_with_vrf(self):
        device = {"cli_style": "ios"}
        result = get_action(device, "tools", "traceroute", vrf="VRF1")
        assert result == "traceroute ip vrf VRF1"

    def test_ios_traceroute_no_vrf(self):
        device = {"cli_style": "ios"}
        result = get_action(device, "tools", "traceroute")
        assert result == "traceroute"

    def test_eos_traceroute_with_vrf(self):
        device = {"cli_style": "eos"}
        result = get_action(device, "tools", "traceroute", vrf="VRF1")
        assert result == "traceroute vrf VRF1"

    def test_junos_traceroute_with_vrf(self):
        device = {"cli_style": "junos"}
        result = get_action(device, "tools", "traceroute", vrf="VRF1")
        assert result == "traceroute routing-instance VRF1"

    def test_routeros_traceroute_no_vrf_variant(self):
        device = {"cli_style": "routeros"}
        result = get_action(device, "tools", "traceroute")
        assert result == "/tool/traceroute count=1"

    def test_routeros_traceroute_ignores_vrf(self):
        """RouterOS has no VRF variant — VRF is silently ignored."""
        device = {"cli_style": "routeros"}
        result = get_action(device, "tools", "traceroute", vrf="VRF1")
        assert result == "/tool/traceroute count=1"


class TestGetAction:
    def test_resolves_ios_ospf_neighbors(self):
        device = {"cli_style": "ios"}
        result = get_action(device, "ospf", "neighbors")
        assert result == "show ip ospf neighbor"

    def test_resolves_eos_with_vrf(self):
        device = {"cli_style": "eos"}
        result = get_action(device, "ospf", "neighbors", vrf="VRF1")
        assert result == "show ip ospf neighbor vrf VRF1"

    def test_resolves_junos_with_vrf(self):
        device = {"cli_style": "junos"}
        result = get_action(device, "ospf", "neighbors", vrf="VRF1")
        assert result == "show ospf neighbor instance VRF1"

    def test_unknown_cli_style_raises(self):
        device = {"cli_style": "unknown"}
        with pytest.raises(KeyError):
            get_action(device, "ospf", "neighbors")

    def test_unknown_category_raises(self):
        device = {"cli_style": "ios"}
        with pytest.raises(KeyError):
            get_action(device, "bgp", "neighbors")

    def test_vrf_from_device_fallback(self):
        device = {"cli_style": "eos", "vrf": "VRF1"}
        result = get_action(device, "ospf", "neighbors")
        assert "VRF1" in result

    def test_explicit_vrf_overrides_device(self):
        device = {"cli_style": "eos", "vrf": "VRF1"}
        result = get_action(device, "ospf", "neighbors", vrf="VRF2")
        assert "VRF2" in result
        assert "VRF1" not in result
