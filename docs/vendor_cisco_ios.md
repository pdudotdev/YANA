# OSPF on Cisco IOS / IOS-XE

## Configuration Syntax

```
router ospf <process-id>
 router-id <x.x.x.x>
 network <network> <wildcard> area <area-id>
 area <area-id> stub [no-summary]
 area <area-id> nssa [no-summary] [default-information-originate]
 area <area-id> range <network> <mask> [not-advertise]
 passive-interface <interface>
 default-information originate [always] [metric <value>] [metric-type <1|2>]
 redistribute <protocol> [subnets] [metric <value>] [metric-type <1|2>] [route-map <name>]
```

OSPF process ID is locally significant — it does not need to match between neighbors.

## Verification Commands

| Command | Purpose |
|---------|---------|
| `show ip ospf neighbor` | Neighbor state, router-id, interface, dead time |
| `show ip ospf interface` | Per-interface: area, timers, network type, cost, auth, passive |
| `show ip ospf database` | Full LSDB — all LSA types with age, router-id, sequence |
| `show ip ospf` | Process details: router-id, SPF stats, ABR/ASBR role |
| `show ip ospf border-routers` | ABR and ASBR reachability |
| `show running-config \| section ospf` | Current OSPF configuration |

## IOS-Specific Defaults and Behaviors

- **Reference bandwidth**: 100 Mbps by default. All interfaces >= 100 Mbps get cost 1. Use `auto-cost reference-bandwidth <mbps>` to adjust for modern link speeds.
- **Network type defaults**: Ethernet = broadcast, Serial = point-to-point, Tunnel = point-to-point.
- **MTU handling**: OSPF checks MTU in DD packets by default. Use `ip ospf mtu-ignore` to disable (not recommended — masks real problems).
- **Authentication**: Supports plaintext (`ip ospf authentication`) and MD5 (`ip ospf authentication message-digest` + `ip ospf message-digest-key <id> md5 <key>`).
- **VRF handling**: OSPF process is bound to a VRF with `router ospf <id> vrf <name>`. Show commands display all VRFs by default.
- **Passive interface**: Suppresses Hello sending but still advertises the interface's subnet.

## Common Gotchas on IOS

- Forgetting `subnets` keyword on `redistribute` causes only classful networks to be redistributed.
- `area range` on a non-ABR device has no effect — it only works on ABRs.
- Duplicate Router IDs cause EXSTART deadlock. Router ID is chosen from: (1) manual `router-id`, (2) highest loopback IP, (3) highest physical IP.
- The `network` statement uses wildcard masks, not subnet masks (`0.0.0.255` not `255.255.255.0`).
- `clear ip ospf process` is required after changing router-id (disruptive — drops all adjacencies).
