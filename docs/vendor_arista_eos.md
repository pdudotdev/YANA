# OSPF on Arista EOS

## Configuration Syntax

```
router ospf <process-id>
   router-id <x.x.x.x>
   network <network>/<prefix-len> area <area-id>
   area <area-id> stub [no-summary]
   area <area-id> nssa [no-summary] [default-information-originate]
   area <area-id> range <network>/<prefix-len> [not-advertise]
   passive-interface <interface>
   redistribute <protocol> [route-map <name>]
   max-lsa <number>
!
interface <name>
   ip ospf area <area-id>
   ip ospf cost <value>
   ip ospf network point-to-point
```

EOS supports both `network` statements and per-interface `ip ospf area` assignment. The per-interface method is preferred and more explicit.

## VRF Configuration

```
router ospf <process-id> vrf <vrf-name>
   router-id <x.x.x.x>
   network <network>/<prefix-len> area <area-id>
```

VRF-aware show commands append `vrf <name>` at the end:
- `show ip ospf neighbor vrf VRF1`
- `show ip ospf database vrf VRF1`
- `show ip ospf interface vrf VRF1`

## Verification Commands

| Command | Purpose |
|---------|---------|
| `show ip ospf neighbor [vrf <name>]` | Neighbor state and adjacency details |
| `show ip ospf interface [vrf <name>]` | Interface parameters, timers, area |
| `show ip ospf database [vrf <name>]` | Full LSDB contents |
| `show ip ospf [vrf <name>]` | Process overview, router-id, SPF |
| `show running-config section ospf` | Current OSPF configuration |

## EOS-Specific Defaults and Behaviors

- **Reference bandwidth**: 100 Mbps default (same as IOS). Adjust with `auto-cost reference-bandwidth`.
- **Network type defaults**: Same as IOS — Ethernet = broadcast, Tunnel = point-to-point.
- **Max-LSA protection**: EOS supports `max-lsa` to limit LSDB size and protect CPU.
- **BFD integration**: `ip ospf bfd` on interface enables BFD for fast failure detection.
- **Section filter**: EOS uses `section` keyword directly (no pipe): `show running-config section ospf`.

## Common Gotchas on EOS

- VRF must be specified in show commands to see VRF-specific OSPF data — `show ip ospf neighbor` without VRF shows only default VRF.
- EOS uses CIDR notation (`/24`) in network statements, not wildcard masks.
- Interface-level `ip ospf area` takes precedence over `network` statements under `router ospf`.
- On multi-chassis (MLAG) setups, ensure OSPF router-id is unique per chassis.
