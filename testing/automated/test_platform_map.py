"""UT-002: Platform map structure and VRF resolution."""
import pytest

from platforms.platform_map import PLATFORM_MAP, _apply_vrf, get_action

EXPECTED_CLI_STYLES = {"ios", "eos", "junos", "aos", "routeros", "vyos"}
OSPF_QUERIES = {"neighbors", "database", "borders", "config", "interfaces", "details"}


class TestPlatformMapStructure:
    def test_all_vendors_present(self):
        assert set(PLATFORM_MAP.keys()) == EXPECTED_CLI_STYLES

    @pytest.mark.parametrize("cli_style", EXPECTED_CLI_STYLES)
    def test_ospf_queries_complete(self, cli_style):
        ospf = PLATFORM_MAP[cli_style]["ospf"]
        assert set(ospf.keys()) == OSPF_QUERIES, f"{cli_style} missing OSPF queries"

    @pytest.mark.parametrize("cli_style", EXPECTED_CLI_STYLES)
    def test_interfaces_present(self, cli_style):
        assert "interface_status" in PLATFORM_MAP[cli_style]["interfaces"]


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

    def test_vrf_from_device_fallback(self):
        device = {"cli_style": "eos", "vrf": "VRF1"}
        result = get_action(device, "ospf", "neighbors")
        assert "VRF1" in result

    def test_explicit_vrf_overrides_device(self):
        device = {"cli_style": "eos", "vrf": "VRF1"}
        result = get_action(device, "ospf", "neighbors", vrf="VRF2")
        assert "VRF2" in result
        assert "VRF1" not in result
