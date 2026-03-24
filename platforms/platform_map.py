"""Vendor CLI command mapping — OSPF and interfaces only."""

PLATFORM_MAP = {
    # ── Cisco IOS-XE ─────────────────────────────────────────────────────
    # IOS handles VRF at the OSPF process level — show commands don't take a VRF keyword.
    "ios": {
        "ospf": {
            "neighbors":  "show ip ospf neighbor",
            "database":   "show ip ospf database",
            "borders":    "show ip ospf border-routers",
            "config":     "show running-config | section ospf",
            "interfaces": "show ip ospf interface",
            "details":    "show ip ospf",
        },
        "interfaces": {
            "interface_status": "show ip interface brief",
        },
    },

    # ── Arista EOS ───────────────────────────────────────────────────────
    "eos": {
        "ospf": {
            "neighbors":  {"default": "show ip ospf neighbor",       "vrf": "show ip ospf neighbor vrf {vrf}"},
            "database":   {"default": "show ip ospf database",       "vrf": "show ip ospf database vrf {vrf}"},
            "borders":    {"default": "show ip ospf border-routers", "vrf": "show ip ospf border-routers vrf {vrf}"},
            "config":     "show running-config section ospf",
            "interfaces": {"default": "show ip ospf interface",      "vrf": "show ip ospf interface vrf {vrf}"},
            "details":    {"default": "show ip ospf",                "vrf": "show ip ospf vrf {vrf}"},
        },
        "interfaces": {
            "interface_status": "show ip interface brief",
        },
    },

    # ── Juniper JunOS ────────────────────────────────────────────────────
    "junos": {
        "ospf": {
            "neighbors":  {"default": "show ospf neighbor",  "vrf": "show ospf neighbor instance {vrf}"},
            "database":   {"default": "show ospf database",  "vrf": "show ospf database instance {vrf}"},
            "borders":    {"default": "show ospf route abr", "vrf": "show ospf route abr instance {vrf}"},
            "config":     {"default": "show ospf overview",  "vrf": "show ospf overview instance {vrf}"},
            "interfaces": {"default": "show ospf interface", "vrf": "show ospf interface instance {vrf}"},
            "details":    {"default": "show ospf overview",  "vrf": "show ospf overview instance {vrf}"},
        },
        "interfaces": {
            "interface_status": "show interfaces terse",
        },
    },

    # ── Aruba AOS-CX ────────────────────────────────────────────────────
    "aos": {
        "ospf": {
            "neighbors":  {"default": "show ip ospf neighbors",      "vrf": "show ip ospf neighbors vrf {vrf}"},
            "database":   {"default": "show ip ospf lsdb",           "vrf": "show ip ospf lsdb vrf {vrf}"},
            "borders":    {"default": "show ip ospf border-routers", "vrf": "show ip ospf border-routers vrf {vrf}"},
            "config":     {"default": "show ip ospf",                "vrf": "show ip ospf vrf {vrf}"},
            "interfaces": {"default": "show ip ospf interface",      "vrf": "show ip ospf interface vrf {vrf}"},
            "details":    {"default": "show ip ospf",                "vrf": "show ip ospf vrf {vrf}"},
        },
        "interfaces": {
            "interface_status": "show interface brief",
        },
    },

    # ── MikroTik RouterOS 7 ─────────────────────────────────────────────
    "routeros": {
        "ospf": {
            "neighbors":  "/routing ospf neighbor print terse without-paging",
            "database":   "/routing ospf lsa print without-paging",
            "borders":    "/routing ospf instance print without-paging",
            "config":     "/routing ospf area print detail without-paging",
            "interfaces": "/routing ospf interface print terse without-paging",
            "details":    "/routing ospf instance print detail without-paging",
        },
        "interfaces": {
            "interface_status": "/interface print brief without-paging",
        },
    },

    # ── VyOS (FRRouting) ────────────────────────────────────────────────
    "vyos": {
        "ospf": {
            "neighbors":  {"default": "show ip ospf neighbor",       "vrf": "show ip ospf vrf {vrf} neighbor"},
            "database":   {"default": "show ip ospf database",       "vrf": "show ip ospf vrf {vrf} database"},
            "borders":    {"default": "show ip ospf border-routers", "vrf": "show ip ospf vrf {vrf} border-routers"},
            "config":     "show configuration commands | match ospf",
            "interfaces": {"default": "show ip ospf interface",      "vrf": "show ip ospf vrf {vrf} interface"},
            "details":    {"default": "show ip ospf",                "vrf": "show ip ospf vrf {vrf}"},
        },
        "interfaces": {
            "interface_status": "show interfaces",
        },
    },
}


def _apply_vrf(action, vrf_name: str | None):
    """Apply VRF substitution to an action entry."""
    if isinstance(action, dict) and "default" in action and "vrf" in action:
        template = action["vrf"] if vrf_name else action["default"]
        return template.replace("{vrf}", vrf_name) if vrf_name else template

    if isinstance(action, str) and vrf_name and "{vrf}" in action:
        return action.replace("{vrf}", vrf_name)

    return action


def get_action(device: dict, category: str, query: str, vrf: str | None = None) -> str:
    """Look up vendor-specific CLI command from PLATFORM_MAP with VRF resolution."""
    vrf_name = vrf or device.get("vrf")

    map_entry = PLATFORM_MAP.get(device["cli_style"])
    if not map_entry:
        raise KeyError(f"No platform map for cli_style={device['cli_style']!r}")

    action = map_entry[category][query]
    return _apply_vrf(action, vrf_name)
