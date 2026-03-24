# OSPF on Juniper JunOS

## Configuration Syntax

JunOS uses hierarchical set-style configuration:

```
set protocols ospf area <area-id> interface <interface-name>
set protocols ospf area <area-id> interface <interface-name> metric <cost>
set protocols ospf area <area-id> interface <interface-name> passive
set protocols ospf area <area-id> interface <interface-name> interface-type p2p
set protocols ospf area <area-id> stub [no-summaries]
set protocols ospf area <area-id> nssa [no-summaries] [default-lsa default-metric <metric>]
set protocols ospf area <area-id> area-range <prefix>/<len> [restrict]
```

Key differences from IOS:
- Interfaces are assigned to areas directly (no `network` statement).
- `passive` is per-interface under the area block, not a global statement.
- `no-summaries` (plural) instead of IOS `no-summary`.
- `restrict` on area-range is equivalent to IOS `not-advertise`.

## VRF (Routing Instance) Configuration

```
set routing-instances <vrf-name> instance-type vrf
set routing-instances <vrf-name> protocols ospf area <area-id> interface <interface>
```

VRF-aware show commands use `instance <vrf-name>`:
- `show ospf neighbor instance VRF1`
- `show ospf database instance VRF1`
- `show ospf interface instance VRF1`

## Verification Commands

| Command | Purpose |
|---------|---------|
| `show ospf neighbor [instance <vrf>]` | Neighbor state and adjacency |
| `show ospf interface [instance <vrf>]` | Interface parameters, area, timers |
| `show ospf database [instance <vrf>]` | LSDB contents |
| `show ospf overview [instance <vrf>]` | Process details, router-id, areas |
| `show ospf route abr [instance <vrf>]` | ABR/ASBR reachability |

Note: JunOS uses `show ospf` (no `ip` prefix).

## JunOS-Specific Defaults and Behaviors

- **Reference bandwidth**: 100 Mbps default. Change with `reference-bandwidth <bps>` (in bps, not Mbps: `1g` = 1 Gbps).
- **Router ID**: Selected from highest loopback IP if `lo0.0` exists; otherwise highest interface IP. Explicit `router-id` under `routing-options` is recommended.
- **Authentication**: Configured per-interface: `set protocols ospf area 0 interface et-0/0/0 authentication md5 <key-id> key <secret>`.
- **Graceful restart**: Enabled by default on JunOS. Allows non-stop routing during control plane restarts.
- **Export policy**: JunOS requires an explicit `export` policy to redistribute routes into OSPF (no implicit `redistribute` command).

## Common Gotchas on JunOS

- JunOS does NOT show OSPF data without `instance` if OSPF runs inside a routing-instance. Always specify the instance name.
- `show ospf overview` is the equivalent of IOS `show ip ospf` — shows router-id, area types, and process details.
- The `lo0.0` interface must be explicitly added to an OSPF area to advertise the loopback.
- Stub area keyword is `no-summaries` (plural), not `no-summary`.
- JunOS uses `interface-type p2p` instead of IOS `ip ospf network point-to-point`.
