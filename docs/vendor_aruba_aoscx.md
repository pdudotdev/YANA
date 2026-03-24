# OSPF on Aruba AOS-CX

## Configuration Syntax

```
router ospf <process-id> [vrf <vrf-name>]
    router-id <x.x.x.x>
    area <area-id>
    area <area-id> stub [no-summary]
    area <area-id> nssa [no-summary]
!
interface <name>
    ip ospf <process-id> area <area-id>
    ip ospf cost <value>
    ip ospf network point-to-point
    ip ospf authentication message-digest
    ip ospf message-digest-key <id> md5 <key>
```

AOS-CX uses per-interface OSPF area assignment (similar to EOS). The `network` statement approach is not used.

## VRF Configuration

```
router ospf <process-id> vrf <vrf-name>
    router-id <x.x.x.x>
    area <area-id>
```

VRF-aware show commands append `vrf <name>`:
- `show ip ospf neighbors vrf <name>`
- `show ip ospf lsdb vrf <name>`
- `show ip ospf interface vrf <name>`

Note: AOS-CX uses `neighbors` (plural) and `lsdb` instead of `database`.

## Verification Commands

| Command | Purpose |
|---------|---------|
| `show ip ospf neighbors [vrf <name>]` | Neighbor state (note: plural "neighbors") |
| `show ip ospf interface [vrf <name>]` | Interface OSPF parameters |
| `show ip ospf lsdb [vrf <name>]` | LSDB contents (note: "lsdb" not "database") |
| `show ip ospf [vrf <name>]` | Process overview and configuration |
| `show ip ospf border-routers [vrf <name>]` | ABR/ASBR reachability |
| `show interface brief` | Interface status (note: no "ip" prefix) |

## AOS-CX-Specific Defaults and Behaviors

- **Reference bandwidth**: 40 Gbps default (much higher than IOS/EOS 100 Mbps). This means 1G and 10G interfaces get higher cost values by default.
- **Interface assignment**: OSPF area is assigned per-interface. No `network` statement.
- **Default VRF**: AOS-CX names its default VRF `default`. When OSPF runs in the default VRF, no `vrf` keyword is needed in show commands.
- **Command differences**: `show ip ospf neighbors` (plural), `show ip ospf lsdb` (not `database`), `show interface brief` (no `ip`).

## Common Gotchas on AOS-CX

- The plural `neighbors` in show commands — `show ip ospf neighbors` not `show ip ospf neighbor`.
- `lsdb` keyword instead of `database` for LSDB inspection.
- `show interface brief` has no `ip` prefix (unlike IOS/EOS `show ip interface brief`).
- Higher default reference bandwidth means cost values differ from IOS/EOS for the same link speed.
- When running OSPF in the default VRF, omit the `vrf` keyword from show commands.
