# OSPF on MikroTik RouterOS 7

## Configuration Syntax

RouterOS 7 uses a path-based CLI completely different from IOS-style vendors:

```
/routing ospf instance
add name=default router-id=1.1.1.1

/routing ospf area
add name=backbone instance=default area-id=0.0.0.0
add name=area1 instance=default area-id=0.0.0.1 type=stub

/routing ospf interface-template
add area=backbone networks=10.0.0.0/30 type=ptp
add area=area1 networks=10.1.1.0/24 type=broadcast passive
```

Key differences from IOS-style:
- Configuration is object-based: instances, areas, and interface-templates are separate objects.
- `interface-template` uses `networks` to match interfaces (similar to IOS `network` statement).
- Area type is set on the area object: `type=stub`, `type=nssa`.
- `passive` is a flag on the interface-template, not a separate command.

## VRF (Routing Table) Configuration

RouterOS uses "routing-table" for VRF:

```
/routing ospf instance
add name=vrf1-ospf router-id=1.1.1.1 routing-table=VRF1

/routing ospf area
add name=vrf1-area0 instance=vrf1-ospf area-id=0.0.0.0
```

RouterOS OSPF commands do not have VRF-specific show variants. All instances are shown together.

## Verification Commands

| Command | Purpose |
|---------|---------|
| `/routing ospf neighbor print terse without-paging` | Neighbor state and adjacency |
| `/routing ospf interface print terse without-paging` | OSPF-enabled interfaces |
| `/routing ospf lsa print without-paging` | LSDB (LSA database) |
| `/routing ospf instance print detail without-paging` | Instance details, router-id |
| `/routing ospf area print detail without-paging` | Area configuration |
| `/interface print brief without-paging` | Interface status |

Note: Always append `without-paging` for scripted/SSH access to disable interactive pagination.

## RouterOS-Specific Defaults and Behaviors

- **Router ID**: Must be explicitly configured on the instance. No automatic selection from interface IPs.
- **Network matching**: `interface-template` with `networks=` matches interfaces by their IP subnet. The template is applied to any interface whose address falls within the specified network.
- **Point-to-point**: Use `type=ptp` (not `point-to-point`).
- **Cost**: Set on interface-template with `cost=<value>`.
- **Authentication**: `authentication=md5` and `authentication-key=<key>` on the interface-template.
- **No `show` keyword**: RouterOS uses `/routing ospf neighbor print` style, not `show ip ospf neighbor`.

## Common Gotchas on RouterOS

- Forgetting `without-paging` causes SSH sessions to hang waiting for user input.
- The `+ct` suffix on username (used in SSH automation) disables colors and auto-completion for clean output parsing.
- RouterOS 7 OSPF configuration is completely restructured from RouterOS 6. Old ROS6 commands (`/routing ospf network add`) do not work.
- `terse` flag on `print` gives compact tabular output; `detail` gives verbose key-value output.
- LSA database uses `lsa` keyword, not `database`.
- Interface-template `networks` uses CIDR notation and matches by subnet, not by interface name.
