# Platform Coverage Results
*Generated: 2026-03-28 19:03:34 UTC*

## Summary

| Device | Platform | CLI Style | Tests | Passed | Empty | Failed |
|--------|----------|-----------|-------|--------|-------|--------|
| D1C | cisco_iosxe | ios | 13 | 11 | 2 | 0 |
| A2A | arista_eos | eos | 13 | 10 | 3 | 0 |
| C1J | juniper_junos | junos | 13 | 11 | 2 | 0 |
| D2B | aruba_aoscx | aos | 13 | 11 | 2 | 0 |
| A1M | mikrotik_routeros | routeros | 13 | 13 | 0 | 0 |
| **Total** | | | **65** | **56** | **9** | **0** |

## Detailed Results

### D1C — cisco_iosxe (ios)

#### 1. ospf — neighbors — PASS
Command: `show ip ospf neighbor`
```
Neighbor ID     Pri   State           Dead Time   Address         Interface
22.22.22.22       1   FULL/BDR        00:00:31    10.0.0.10       Ethernet1/2
22.22.22.11     128   FULL/BDR        00:00:39    10.0.0.6        Ethernet1/3
11.11.11.22       1   FULL/BDR        00:00:35    10.0.0.2        Ethernet1/1
4.4.4.4         128   FULL/BDR        00:00:33    10.1.1.25       Ethernet1/0
3.3.3.3           1   FULL/BDR        00:00:31    10.1.1.17       Ethernet0/3
2.2.2.2           1   FULL/BDR        00:00:30    10.1.1.9        Ethernet0/2
1.1.1.1         128   FULL/BDR        00:00:33    10.1.1.1        Ethernet0/1
```

#### 2. ospf — database — PASS
Command: `show ip ospf database`
```
            OSPF Router with ID (11.11.11.11) (Process ID 1)

		Router Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum Link count
9.9.9.9         9.9.9.9         1166        0x8000001C 0x009D88 2         
11.11.11.11     11.11.11.11     1019        0x80000022 0x00A47C 3         
11.11.11.22     11.11.11.22     480         0x8000001F 0x000CF2 3         
22.22.22.11     22.22.22.11     2276        0x80000016 0x0027F7 5         
22.22.22.22     22.22.22.22     808         0x80000021 0x00011C 6         
33.33.33.11     33.33.33.11     1056        0x80000020 0x001A6B 2         
33.33.33.22     33.33.33.22     1259        0x8000001F 0x00411F 2         

		Net Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum
10.0.0.1        11.11.11.11     1263        0x80000018 0x00C1C9
10.0.0.5        11.11.11.11     1019        0x80000018 0x008CE4
10.0.0.9        11.11.11.11     1263        0x80000018 0x00FE63
10.0.0.13       11.11.11.22     480         0x8000001B 0x00EB84
10.0.0.18       22.22.22.22     1228        0x8000001A 0x003FE0
10.0.0.22       22.22.22.22     808         0x8000001A 0x000AFB
10.0.0.26       33.33.33.11     1056        0x80000018 0x00B91E
10.0.0.30       33.33.33.22     1259        0x80000018 0x00BDFF
10.0.0.33       22.22.22.22     1048        0x8000001A 0x0029B0
10.0.0.37       22.22.22.22     1048        0x8000001A 0x009B2F
10.0.0.42       22.22.22.22     1228        0x8000001A 0x004FCB

		Summary Net Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum
10.1.1.0        11.11.11.11     1263        0x80000018 0x00DA09
10.1.1.0        11.11.11.22     790         0x8000001E 0x005A34
192.168.41.1    11.11.11.11     1263        0x80000018 0x00FD5D
192.168.41.1    11.11.11.22     820         0x8000001B 0x001FF3
192.168.42.1    11.11.11.11     1263        0x80000018 0x004D04
192.168.42.1    11.11.11.22     790         0x8000001C 0x006C9B
192.168.43.1    11.11.11.11     1263        0x80000018 0x00420E
192.168.43.1    11.11.11.22     794         0x8000001C 0x0061A5
192.168.44.1    11.11.11.11     1263        0x80000018 0x00DC7B
192.168.44.1    11.11.11.22     815         0x8000001C 0x00FB13

		Router Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum Link count
1.1.1.1         1.1.1.1         639         0x8000001F 0x0062DA 3         
2.2.2.2         2.2.2.2         1106        0x8000001D 0x00CE0C 3         
3.3.3.3         3.3.3.3         1107        0x8000001D 0x00A30E 3         
4.4.4.4         4.4.4.4         837         0x8000001F 0x00A71A 3         
11.11.11.11     11.11.11.11     1263        0x80000023 0x00068E 4         
11.11.11.22     11.11.11.22     786         0x80000021 0x00E832 4         

		Net Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum
10.1.1.2        11.11.11.11     1263        0x80000018 0x002E8F
10.1.1.5        1.1.1.1         851         0x8000001B 0x0054A0
10.1.1.10       11.11.11.11     1263        0x80000018 0x0010A1
10.1.1.13       2.2.2.2         1106        0x8000001A 0x00289D
10.1.1.18       11.11.11.11     1263        0x80000018 0x00F1B3
10.1.1.21       3.3.3.3         1107        0x8000001A 0x00DBD9
10.1.1.26       11.11.11.11     1263        0x80000018 0x00D3C5
10.1.1.29       4.4.4.4         649         0x8000001B 0x006F55

		Summary Net Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum
0.0.0.0         11.11.11.11     1263        0x80000018 0x0038C2
0.0.0.0         11.11.11.22     831         0x8000001B 0x00D13B
10.0.0.0        11.11.11.11     1263        0x80000018 0x00FDEC
10.0.0.0        11.11.11.22     835         0x8000001B 0x001F83
10.0.0.4        11.11.11.11     1263        0x80000018 0x00D511
10.0.0.4        11.11.11.22     474         0x8000001C 0x00FE9D
10.0.0.8        11.11.11.11     1263        0x80000018 0x00AD35
10.0.0.8        11.11.11.22     826         0x8000001B 0x00335D
10.0.0.12       11.11.11.11     1019        0x8000001A 0x008B50
10.0.0.12       11.11.11.22     835         0x8000001B 0x00A6EF
10.0.0.16       11.11.11.11     1263        0x80000018 0x00C10F
10.0.0.16       11.11.11.22     836         0x8000001B 0x007E14
10.0.0.20       11.11.11.11     1019        0x80000019 0x003D97
10.0.0.20       11.11.11.22     474         0x8000001D 0x005C2F
10.0.0.24       11.11.11.11     1019        0x80000019 0x0015BB
10.0.0.24       11.11.11.22     474         0x8000001C 0x003652
10.0.0.28       11.11.11.11     1019        0x80000019 0x00ECDF
10.0.0.28       11.11.11.22     474         0x8000001C 0x000E76
10.0.0.32       11.11.11.11     1019        0x80000019 0x00CEF8
10.0.0.32       11.11.11.22     474         0x8000001D 0x00ED90
10.0.0.36       11.11.11.11     1019        0x80000019 0x00A61D
10.0.0.36       11.11.11.22     474         0x8000001D 0x00C5B4
10.0.0.40       11.11.11.11     1263        0x80000018 0x00D0E7
10.0.0.40       11.11.11.22     816         0x8000001C 0x00EF7F
10.9.9.1        11.11.11.11     1263        0x80000018 0x00FEC1
10.9.9.1        11.11.11.22     816         0x8000001B 0x002058

		Type-5 AS External Link States

Link ID         ADV Router      Age         Seq#       Checksum Tag
0.0.0.0         33.33.33.11     1306        0x80000018 0x002C81 1         
0.0.0.0         33.33.33.22     1259        0x80000018 0x00E9B8 1         
10.10.10.0      11.11.11.11     1263        0x80000018 0x006F53 0         
... (4 more lines truncated)
```

#### 3. ospf — borders — PASS
Command: `show ip ospf border-routers`
```
            OSPF Router with ID (11.11.11.11) (Process ID 1)


		Base Topology (MTID 0)

Internal Router Routing Table
Codes: i - Intra-area route, I - Inter-area route

i 9.9.9.9 [20] via 10.0.0.10, Ethernet1/2, ASBR, Area 0, SPF 32
i 33.33.33.11 [11] via 10.0.0.6, Ethernet1/3, ASBR, Area 0, SPF 32
i 33.33.33.22 [11] via 10.0.0.6, Ethernet1/3, ASBR, Area 0, SPF 32
i 22.22.22.22 [10] via 10.0.0.10, Ethernet1/2, ASBR, Area 0, SPF 32
i 11.11.11.22 [11] via 10.1.1.25, Ethernet1/0, ABR, Area 1, SPF 20
i 11.11.11.22 [10] via 10.0.0.2, Ethernet1/1, ABR, Area 0, SPF 32
i 11.11.11.22 [11] via 10.1.1.1, Ethernet0/1, ABR, Area 1, SPF 20
```

#### 4. ospf — config — PASS
Command: `show running-config | section ospf`
```
  redistribute ospf 1 route-map OSPF-TO-EIGRP
router ospf 1 vrf VRF1
 router-id 11.11.11.11
 area 1 stub
 area 1 range 10.1.1.0 255.255.255.0
 redistribute eigrp 10 metric-type 1
 network 10.0.0.0 0.0.0.3 area 0
 network 10.0.0.4 0.0.0.3 area 0
 network 10.0.0.8 0.0.0.3 area 0
 network 10.1.1.0 0.0.0.3 area 1
 network 10.1.1.8 0.0.0.3 area 1
 network 10.1.1.16 0.0.0.3 area 1
 network 10.1.1.24 0.0.0.3 area 1
```

#### 5. ospf — interfaces — PASS
Command: `show ip ospf interface`
```
Ethernet1/2 is up, line protocol is up 
  Internet Address 10.0.0.9/30, Interface ID 8, Area 0
  Attached via Network Statement
  Process ID 1, Router ID 11.11.11.11, Network Type BROADCAST, Cost: 10
  Topology-MTID    Cost    Disabled    Shutdown      Topology Name
        0           10        no          no            Base
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 11.11.11.11, Interface address 10.0.0.9
  Backup Designated router (ID) 22.22.22.22, Interface address 10.0.0.10
  Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
    oob-resync timeout 40
    Hello due in 00:00:08
  Supports Link-local Signaling (LLS)
  Cisco NSF helper support enabled
  IETF NSF helper support enabled
  Can be protected by per-prefix Loop-Free FastReroute
  Can be used for per-prefix Loop-Free FastReroute repair paths
  Not Protected by per-prefix TI-LFA
  Index 1/3/3, flood queue length 0
  Next 0x0(0)/0x0(0)/0x0(0)
  Last flood scan length is 2, maximum is 12
  Last flood scan time is 0 msec, maximum is 1 msec
  Neighbor Count is 1, Adjacent neighbor count is 1 
    Adjacent with neighbor 22.22.22.22  (Backup Designated Router)
  Suppress hello for 0 neighbor(s)
Ethernet1/3 is up, line protocol is up 
  Internet Address 10.0.0.5/30, Interface ID 9, Area 0
  Attached via Network Statement
  Process ID 1, Router ID 11.11.11.11, Network Type BROADCAST, Cost: 10
  Topology-MTID    Cost    Disabled    Shutdown      Topology Name
        0           10        no          no            Base
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 11.11.11.11, Interface address 10.0.0.5
  Backup Designated router (ID) 22.22.22.11, Interface address 10.0.0.6
  Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
    oob-resync timeout 40
    Hello due in 00:00:01
  Supports Link-local Signaling (LLS)
  Cisco NSF helper support enabled
  IETF NSF helper support enabled
  Can be protected by per-prefix Loop-Free FastReroute
  Can be used for per-prefix Loop-Free FastReroute repair paths
  Not Protected by per-prefix TI-LFA
  Index 1/2/2, flood queue length 0
  Next 0x0(0)/0x0(0)/0x0(0)
  Last flood scan length is 2, maximum is 12
  Last flood scan time is 0 msec, maximum is 1 msec
  Neighbor Count is 1, Adjacent neighbor count is 1 
    Adjacent with neighbor 22.22.22.11  (Backup Designated Router)
  Suppress hello for 0 neighbor(s)
Ethernet1/1 is up, line protocol is up 
  Internet Address 10.0.0.1/30, Interface ID 7, Area 0
  Attached via Network Statement
  Process ID 1, Router ID 11.11.11.11, Network Type BROADCAST, Cost: 10
  Topology-MTID    Cost    Disabled    Shutdown      Topology Name
        0           10        no          no            Base
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 11.11.11.11, Interface address 10.0.0.1
  Backup Designated router (ID) 11.11.11.22, Interface address 10.0.0.2
  Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
    oob-resync timeout 40
    Hello due in 00:00:08
  Supports Link-local Signaling (LLS)
  Cisco NSF helper support enabled
  IETF NSF helper support enabled
  Can be protected by per-prefix Loop-Free FastReroute
  Can be used for per-prefix Loop-Free FastReroute repair paths
  Not Protected by per-prefix TI-LFA
  Index 1/1/1, flood queue length 0
  Next 0x0(0)/0x0(0)/0x0(0)
  Last flood scan length is 0, maximum is 12
  Last flood scan time is 0 msec, maximum is 1 msec
  Neighbor Count is 1, Adjacent neighbor count is 1 
    Adjacent with neighbor 11.11.11.22  (Backup Designated Router)
  Suppress hello for 0 neighbor(s)
Ethernet1/0 is up, line protocol is up 
  Internet Address 10.1.1.26/30, Interface ID 6, Area 1
  Attached via Network Statement
  Process ID 1, Router ID 11.11.11.11, Network Type BROADCAST, Cost: 10
  Topology-MTID    Cost    Disabled    Shutdown      Topology Name
        0           10        no          no            Base
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 11.11.11.11, Interface address 10.1.1.26
  Backup Designated router (ID) 4.4.4.4, Interface address 10.1.1.25
  Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
    oob-resync timeout 40
    Hello due in 00:00:02
  Supports Link-local Signaling (LLS)
  Cisco NSF helper support enabled
  IETF NSF helper support enabled
  Can be protected by per-prefix Loop-Free FastReroute
  Can be used for per-prefix Loop-Free FastReroute repair paths
  Not Protected by per-prefix TI-LFA
  Index 1/4/7, flood queue length 0
  Next 0x0(0)/0x0(0)/0x0(0)
  Last flood scan length is 6, maximum is 12
  Last flood scan time is 0 msec, maximum is 3 msec
  Neighbor Count is 1, Adjacent neighbor count is 1 
    Adjacent with neighbor 4.4.4.4  (Backup Designated Router)
  Suppress hello for 0 neighbor(s)
... (75 more lines truncated)
```

#### 6. ospf — details — PASS
Command: `show ip ospf`
```
 Routing Process "ospf 1" with ID 11.11.11.11
   Domain ID type 0x0005, value 0.0.0.1
 Start time: 00:00:02.388, Time elapsed: 13:15:55.301
 Supports only single TOS(TOS0) routes
 Supports opaque LSA
 Supports Link-local Signaling (LLS)
 Supports area transit capability
 Supports NSSA (compatible with RFC 3101)
 Supports Database Exchange Summary List Optimization (RFC 5243)
 Connected to MPLS VPN Superbackbone, VRF VRF1
 Maximum number of non self-generated LSA allowed 50000
    Current number of non self-generated LSA 43
    Threshold for warning message 75%
    Ignore-time 5 minutes, reset-time 10 minutes
    Ignore-count allowed 5, current ignore-count 0
 Event-log disabled
 It is an area border and autonomous system boundary router
 Redistributing External Routes from,
    eigrp 10, includes subnets in redistribution
    Maximum limit of redistributed prefixes 10240
    Threshold for warning message 75%
 Router is not originating router-LSAs with maximum metric
 Initial SPF schedule delay 50 msecs
 Minimum hold time between two consecutive SPFs 200 msecs
 Maximum wait time between two consecutive SPFs 5000 msecs
 Incremental-SPF disabled
 Per-prefix-distribution disabled
 Initial LSA throttle delay 50 msecs
 Minimum hold time for LSA throttle 200 msecs
 Maximum wait time for LSA throttle 5000 msecs
 Minimum LSA arrival 100 msecs
 LSA group pacing timer 240 secs
 Interface flood pacing timer 33 msecs
 Retransmission pacing timer 66 msecs
 EXCHANGE/LOADING adjacency limit: initial 300, process maximum 300
 Number of external LSA 7. Checksum Sum 0x02D4B4
 Number of opaque AS LSA 0. Checksum Sum 0x000000
 Number of DCbitless external and opaque AS LSA 0
 Number of DoNotAge external and opaque AS LSA 0
 Number of areas in this router is 2. 1 normal 1 stub 0 nssa
 Number of areas transit capable is 0
 External flood list length 0
 IETF NSF helper support enabled
 Cisco NSF helper support enabled
 Reference bandwidth unit is 100 mbps
    Area BACKBONE(0)
        Number of interfaces in this area is 3
	Area has no authentication
	SPF algorithm last executed 13:08:22.027 ago
	SPF algorithm executed 32 times
	Area ranges are
	Number of LSA 28. Checksum Sum 0x0D6936
	Number of opaque link LSA 0. Checksum Sum 0x000000
	Number of DCbitless LSA 7
	Number of indication LSA 0
	Number of DoNotAge LSA 0
	Flood list length 0
    Area 1
        Number of interfaces in this area is 4
        It is a stub area
        Generates stub default route with cost 1
	Area has no authentication
	SPF algorithm last executed 13:13:39.723 ago
	SPF algorithm executed 20 times
	Area ranges are
	   10.1.1.0/24 Active(10) Advertise 
	Number of LSA 40. Checksum Sum 0x166CEF
	Number of opaque link LSA 0. Checksum Sum 0x000000
	Number of DCbitless LSA 18
	Number of indication LSA 0
	Number of DoNotAge LSA 0
	Flood list length 0
 Maintenance Mode ID:     128920110258832
 Maintenance Mode:        disabled
 Maintenance Mode Timer:  stopped (0)
  Graceful Reload FSU Global status : None (global: None)
```

#### 7. routing_table — ip_route — PASS
Command: `show ip route`
```
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, m - OMP
       n - NAT, Ni - NAT inside, No - NAT outside, Nd - NAT DIA
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       H - NHRP, G - NHRP registered, g - NHRP registration summary
       o - ODR, P - periodic downloaded static route, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR
       & - replicated local route overrides by connected

Gateway of last resort is not set
```

#### 8. routing_table — route_maps — PASS
Command: `show route-map`
```
route-map OSPF-TO-EIGRP, permit, sequence 10
  Match clauses:
  Set clauses:
    metric 1000000 1 255 1 1500
  Policy routing matches: 0 packets, 0 bytes
```

#### 9. routing_table — prefix_lists — EMPTY
Command: `show ip prefix-list`
```

```

#### 10. routing_table — policy_based_routing — PASS
Command: `show route-map`
```
route-map OSPF-TO-EIGRP, permit, sequence 10
  Match clauses:
  Set clauses:
    metric 1000000 1 255 1 1500
  Policy routing matches: 0 packets, 0 bytes
```

#### 11. routing_table — access_lists — EMPTY
Command: `show access-lists`
```

```

#### 12. interfaces — interface_status — PASS
Command: `show ip interface brief`
```
Interface              IP-Address      OK? Method Status                Protocol
Ethernet0/0            172.20.20.205   YES NVRAM  up                    up      
Ethernet0/1            10.1.1.2        YES NVRAM  up                    up      
Ethernet0/2            10.1.1.10       YES NVRAM  up                    up      
Ethernet0/3            10.1.1.18       YES NVRAM  up                    up      
Ethernet1/0            10.1.1.26       YES NVRAM  up                    up      
Ethernet1/1            10.0.0.1        YES NVRAM  up                    up      
Ethernet1/2            10.0.0.9        YES NVRAM  up                    up      
Ethernet1/3            10.0.0.5        YES NVRAM  up                    up      
Ethernet2/0            10.10.10.2      YES NVRAM  up                    up      
Ethernet2/1            10.10.10.6      YES NVRAM  up                    up      
Ethernet2/2            unassigned      YES NVRAM  administratively down down    
Ethernet2/3            unassigned      YES NVRAM  administratively down down    
```

#### 13. tools — traceroute — PASS
Command: `traceroute vrf VRF1 172.20.20.207 probe 1 timeout 2`
```
Type escape sequence to abort.
Tracing the route to 172.20.20.207
VRF info: (vrf in name/id, vrf out name/id)
  1 10.0.0.6 2 msec
  2 10.0.0.26 1 msec
  3  * 
  4  * 
  5  * 
  6  * 
  7  * 
  8  * 
  9  * 
 10  * 
 11  * 
 12  * 
 13  * 
 14  * 
 15  * 
 16  * 
 17  * 
 18  * 
 19  * 
 20  * 
 21  * 
 22  * 
 23  * 
 24  * 
 25  * 
 26  * 
 27  * 
 28  * 
 29  * 
 30  * 
```

### A2A — arista_eos (eos)

#### 1. ospf — neighbors — PASS
Command: `show ip ospf neighbor vrf VRF1`
```
Neighbor ID     Instance VRF      Pri State                  Dead Time   Address         Interface
11.11.11.22     1        VRF1     1   FULL/BDR               00:00:32    10.1.1.14       Ethernet2
11.11.11.11     1        VRF1     1   FULL/DR                00:00:31    10.1.1.10       Ethernet1
```

#### 2. ospf — database — PASS
Command: `show ip ospf database vrf VRF1`
```
            OSPF Router with ID(2.2.2.2) (Instance ID 1) (VRF VRF1)


                 Router Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#         Checksum Link count
3.3.3.3         3.3.3.3         1111        0x8000001d   0xa30e   3
4.4.4.4         4.4.4.4         841         0x8000001f   0xa71a   3
2.2.2.2         2.2.2.2         1108        0x8000001d   0xce0c   3
1.1.1.1         1.1.1.1         643         0x8000001f   0x62da   3
11.11.11.11     11.11.11.11     1267        0x80000023   0x68e    4
11.11.11.22     11.11.11.22     788         0x80000021   0xe832   4

                 Network Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#         Checksum
10.1.1.5        1.1.1.1         855         0x8000001b   0x54a0  
10.1.1.26       11.11.11.11     1267        0x80000018   0xd3c5  
10.1.1.2        11.11.11.11     1267        0x80000018   0x2e8f  
10.1.1.18       11.11.11.11     1267        0x80000018   0xf1b3  
10.1.1.10       11.11.11.11     1267        0x80000018   0x10a1  
10.1.1.29       4.4.4.4         653         0x8000001b   0x6f55  
10.1.1.21       3.3.3.3         1111        0x8000001a   0xdbd9  
10.1.1.13       2.2.2.2         1108        0x8000001a   0x289d  

                 Summary Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#         Checksum
10.0.0.4        11.11.11.11     1267        0x80000018   0xd511  
0.0.0.0         11.11.11.22     833         0x8000001b   0xd13b  
0.0.0.0         11.11.11.11     1267        0x80000018   0x38c2  
10.9.9.1        11.11.11.11     1267        0x80000018   0xfec1  
10.0.0.8        11.11.11.11     1267        0x80000018   0xad35  
10.0.0.16       11.11.11.11     1267        0x80000018   0xc10f  
10.0.0.32       11.11.11.11     1022        0x80000019   0xcef8  
10.0.0.0        11.11.11.11     1267        0x80000018   0xfdec  
10.0.0.0        11.11.11.22     837         0x8000001b   0x1f83  
10.0.0.32       11.11.11.22     475         0x8000001d   0xed90  
10.0.0.16       11.11.11.22     838         0x8000001b   0x7e14  
10.0.0.24       11.11.11.11     1022        0x80000019   0x15bb  
10.0.0.40       11.11.11.11     1267        0x80000018   0xd0e7  
10.0.0.8        11.11.11.22     828         0x8000001b   0x335d  
10.0.0.40       11.11.11.22     820         0x8000001c   0xef7f  
10.0.0.24       11.11.11.22     475         0x8000001c   0x3652  
10.0.0.12       11.11.11.22     837         0x8000001b   0xa6ef  
10.0.0.20       11.11.11.11     1022        0x80000019   0x3d97  
10.0.0.36       11.11.11.11     1022        0x80000019   0xa61d  
10.0.0.4        11.11.11.22     475         0x8000001c   0xfe9d  
10.0.0.36       11.11.11.22     475         0x8000001d   0xc5b4  
10.0.0.20       11.11.11.22     475         0x8000001d   0x5c2f  
10.0.0.28       11.11.11.11     1022        0x80000019   0xecdf  
10.0.0.12       11.11.11.11     1022        0x8000001a   0x8b50  
10.0.0.28       11.11.11.22     475         0x8000001c   0xe76   
10.9.9.1        11.11.11.22     820         0x8000001b   0x2058  
```

#### 3. ospf — borders — PASS
Command: `show ip ospf border-routers vrf VRF1`
```
OSPF instance 1 with ID 2.2.2.2, VRF VRF1
Router ID       Area            Type            Cost
11.11.11.11     0.0.0.1         ABR             10
11.11.11.22     0.0.0.1         ABR             10
```

#### 4. ospf — config — PASS
Command: `show running-config section ospf`
```
router ospf 1 vrf VRF1
   router-id 2.2.2.2
   area 0.0.0.1 stub
   network 10.1.1.0/24 area 0.0.0.1
   network 192.168.42.1/32 area 0.0.0.1
   max-lsa 12000
```

#### 5. ospf — interfaces — PASS
Command: `show ip ospf interface vrf VRF1`
```
Loopback0 is up
  Interface Address 192.168.42.1/32, instance 1, VRF VRF1, Area 0.0.0.1
  Network Type Broadcast, Cost: 10
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router is 2.2.2.2
  No Backup Designated Router on this network
  Timer intervals configured, Hello 10, Dead 40, Retransmit 5
  Neighbor Count is 0
  No authentication
  Traffic engineering is disabled
  TI-LFA protection is disabled
Ethernet2 is up
  Interface Address 10.1.1.13/30, instance 1, VRF VRF1, Area 0.0.0.1
  Network Type Broadcast, Cost: 10
  Transmit Delay is 1 sec, State DR, Priority 1
  Interface Speed: 1000 mbps
  Designated Router is 2.2.2.2
  Backup Designated Router is 11.11.11.22
  Timer intervals configured, Hello 10, Dead 40, Retransmit 5
  Neighbor Count is 1
  No authentication
  Traffic engineering is disabled
  TI-LFA protection is disabled
Ethernet1 is up
  Interface Address 10.1.1.9/30, instance 1, VRF VRF1, Area 0.0.0.1
  Network Type Broadcast, Cost: 10
  Transmit Delay is 1 sec, State Backup DR, Priority 1
  Interface Speed: 1000 mbps
  Designated Router is 11.11.11.11
  Backup Designated Router is 2.2.2.2
  Timer intervals configured, Hello 10, Dead 40, Retransmit 5
  Neighbor Count is 1
  No authentication
  Traffic engineering is disabled
  TI-LFA protection is disabled
```

#### 6. ospf — details — PASS
Command: `show ip ospf vrf VRF1`
```
OSPF instance 1 with ID 2.2.2.2 VRF VRF1
 Supports opaque LSA
Maximum number of LSA allowed 12000
  Threshold for warning message 75%
  Ignore-time 5 minutes, reset-time 5 minutes
  Ignore-count allowed 5, current 0
 It is an autonomous system boundary router and is not an area border router
 Initial SPF schedule delay 0 msecs
 Minimum hold time between two consecutive SPFs 5000 msecs
 Current hold time between two consecutive SPFs 5000 msecs
 Maximum wait time between two consecutive SPFs 5000 msecs
 Minimum LSA arrival 1000 msecs
 Initial LSA throttle delay 1000 msecs
 Minimum hold time for LSA throttle 5000 msecs
 Maximum wait time for LSA throttle 5000 msecs
 Number of external LSA 0, Checksum sum 0
 Number of opaque AS LSA 0, Checksum sum 0
 Number of areas in this router is 1. 0 normal, 1 stub, 0 nssa
 Number of LSA 40
 Time since last SPF 47304 secs
 No Scheduled SPF
 Adjacency exchange-start threshold is 20
 Maximum number of next-hops supported in ECMP is 128
 Retransmission threshold for LSA is 10
 Number of backbone neighbors is 0
 Routes over tunnel interfaces disabled
 Graceful-restart is not configured
 Graceful-restart-helper mode is enabled
 Area 0.0.0.1
 Number of interface in this area is 3
   It is a stub area
   Traffic engineering is disabled
   Area has None authentication 
   SPF algorithm executed 17 times
   Number of LSA 40. Checksum Sum 1469679
   Number of opaque link LSA 0. Checksum Sum 0
   Number of opaque area LSA 0. Checksum Sum 0
   Number of indication LSA 0
   Number of DC-clear LSA 18
```

#### 7. routing_table — ip_route — PASS
Command: `show ip route vrf VRF1`
```
VRF: VRF1
Source Codes:
       C - connected, S - static, K - kernel,
       O - OSPF, O IA - OSPF inter area, O E1 - OSPF external type 1,
       O E2 - OSPF external type 2, O N1 - OSPF NSSA external type 1,
       O N2 - OSPF NSSA external type2, O3 - OSPFv3,
       O3 IA - OSPFv3 inter area, O3 E1 - OSPFv3 external type 1,
       O3 E2 - OSPFv3 external type 2,
       O3 N1 - OSPFv3 NSSA external type 1,
       O3 N2 - OSPFv3 NSSA external type2, B - Other BGP Routes,
       B I - iBGP, B E - eBGP, R - RIP, I L1 - IS-IS level 1,
       I L2 - IS-IS level 2, A B - BGP Aggregate,
       A O - OSPF Summary, NG - Nexthop Group Static Route,
       V - VXLAN Control Service, M - Martian,
       DH - DHCP client installed default route,
       DP - Dynamic Policy Route, L - VRF Leaked,
       G  - gRIBI, RC - Route Cache Route,
       CL - CBF Leaked Route

Gateway of last resort:
 O IA     0.0.0.0/0 [110/11]
           via 10.1.1.10, Ethernet1
           via 10.1.1.14, Ethernet2

 O IA     10.0.0.0/30 [110/20]
           via 10.1.1.10, Ethernet1
 O IA     10.0.0.4/30 [110/20]
           via 10.1.1.10, Ethernet1
 O IA     10.0.0.8/30 [110/20]
           via 10.1.1.10, Ethernet1
 O IA     10.0.0.12/30 [110/21]
           via 10.1.1.10, Ethernet1
 O IA     10.0.0.16/30 [110/30]
           via 10.1.1.10, Ethernet1
 O IA     10.0.0.20/30 [110/21]
           via 10.1.1.10, Ethernet1
 O IA     10.0.0.24/30 [110/21]
           via 10.1.1.10, Ethernet1
 O IA     10.0.0.28/30 [110/21]
           via 10.1.1.10, Ethernet1
 O IA     10.0.0.32/30 [110/22]
           via 10.1.1.10, Ethernet1
 O IA     10.0.0.36/30 [110/22]
           via 10.1.1.10, Ethernet1
 O IA     10.0.0.40/30 [110/30]
           via 10.1.1.10, Ethernet1
 O        10.1.1.0/30 [110/20]
           via 10.1.1.10, Ethernet1
 O        10.1.1.4/30 [110/21]
           via 10.1.1.10, Ethernet1
 C        10.1.1.8/30
           directly connected, Ethernet1
 C        10.1.1.12/30
           directly connected, Ethernet2
 O        10.1.1.16/30 [110/20]
           via 10.1.1.10, Ethernet1
 O        10.1.1.20/30 [110/30]
           via 10.1.1.10, Ethernet1
 O        10.1.1.24/30 [110/20]
           via 10.1.1.10, Ethernet1
 O        10.1.1.28/30 [110/21]
           via 10.1.1.10, Ethernet1
 O IA     10.9.9.1/32 [110/40]
           via 10.1.1.10, Ethernet1
 O        192.168.41.1/32 [110/21]
           via 10.1.1.10, Ethernet1
 C        192.168.42.1/32
           directly connected, Loopback0
 O        192.168.43.1/32 [110/30]
           via 10.1.1.10, Ethernet1
 O        192.168.44.1/32 [110/21]
           via 10.1.1.10, Ethernet1
```

#### 8. routing_table — route_maps — EMPTY
Command: `show route-map`
```

```

#### 9. routing_table — prefix_lists — EMPTY
Command: `show ip prefix-list`
```

```

#### 10. routing_table — policy_based_routing — EMPTY
Command: `show policy-map type pbr`
```

```

#### 11. routing_table — access_lists — PASS
Command: `show ip access-lists`
```
Phone ACL bypass: disabled
IP Access List default-control-plane-acl [readonly]
Warning: displaying stale counters
        counters per-entry
        10 permit icmp any any [match 235032 bytes in 2807 packets, 0:20:16 ago]
        20 permit ip any any tracked [match 674480 bytes in 5029 packets, 0:00:00 ago]
        30 permit udp any any eq bfd ttl eq 255
        40 permit udp any any eq bfd-echo ttl eq 254
        50 permit udp any any eq multihop-bfd micro-bfd sbfd
        60 permit udp any eq sbfd any eq sbfd-initiator
        70 permit ospf any any [match 951216 bytes in 10808 packets, 0:00:00 ago]
        80 permit tcp any any eq ssh telnet www snmp bgp https msdp ldp netconf-ssh gnmi [match 7800 bytes in 130 packets, 0:00:10 ago]
        90 permit udp any any eq bootps bootpc snmp rip ntp ldp ptp-event ptp-general
        100 permit tcp any any eq mlag ttl eq 255
        110 permit udp any any eq mlag ttl eq 255
        120 permit vrrp any any
        130 permit ahp any any
        140 permit pim any any
        150 permit igmp any any
        160 permit tcp any any range 5900 5910
        170 permit tcp any any range 50000 50100
        180 permit udp any any range 51000 51100
        190 permit tcp any any eq 3333
        200 permit tcp any any eq nat ttl eq 255
        210 permit tcp any eq bgp any
        220 permit rsvp any any
        230 permit tcp any any eq 9340
        240 permit tcp any any eq 9559
        250 permit udp any any eq 8503
        260 permit udp any any eq lsp-ping
        270 permit udp any eq lsp-ping any range 51900 51999
        (implicit) deny ip any any

        Total rules configured: 27
        Configured on Ingress: control-plane(VRF1 VRF)
                       control-plane(default VRF)
        Active on     Ingress: control-plane(VRF1 VRF)
                       control-plane(default VRF)
```

#### 12. interfaces — interface_status — PASS
Command: `show ip interface brief`
```
                                                                                 Address
Interface         IP Address             Status       Protocol            MTU    Owner  
----------------- ---------------------- ------------ -------------- ----------- -------
Ethernet1         10.1.1.9/30            up           up                 1500           
Ethernet2         10.1.1.13/30           up           up                 1500           
Loopback0         192.168.42.1/32        up           up                65535           
Management0       172.20.20.202/24       up           up                 1500           
```

#### 13. tools — traceroute — PASS
Command: `traceroute vrf VRF1 172.20.20.207`
```
traceroute to 172.20.20.207 (172.20.20.207), 30 hops max, 60 byte packets
 1  _gateway (10.1.1.10)  0.476 ms  0.487 ms  0.470 ms
 2  10.0.0.6 (10.0.0.6)  3.300 ms  4.752 ms  5.096 ms
 3  10.0.0.26 (10.0.0.26)  3.289 ms  3.470 ms 10.0.0.30 (10.0.0.30)  3.329 ms
 4  * * *
 5  * * *
 6  * * *
 7  * * *
 8  * * *
 9  * * *
10  * * *
11  * * *
12  * * *
13  * * *
14  * * *
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```

### C1J — juniper_junos (junos)

#### 1. ospf — neighbors — PASS
Command: `show ospf neighbor instance VRF1`
```
 

Warning: License key missing; requires 'OSPF' license

Address          Interface              State           ID               Pri  Dead
10.0.0.26        et-0/0/0.0             Full            33.33.33.11        1    31
10.0.0.30        et-0/0/1.0             Full            33.33.33.22        1    32
10.0.0.22        et-0/0/2.0             Full            22.22.22.22        1    33
10.0.0.13        et-0/0/3.0             Full            11.11.11.22        1    32
10.0.0.5         et-0/0/4.0             Full            11.11.11.11        1    39
```

#### 2. ospf — database — PASS
Command: `show ospf database instance VRF1`
```
 

Warning: License key missing; requires 'OSPF' license


    OSPF database, Area 0.0.0.0
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len 
Router   9.9.9.9          9.9.9.9          0x8000001c  1169  0x22 0x9d88  48
Router   11.11.11.11      11.11.11.11      0x80000022  1023  0x22 0xa47c  60
Router   11.11.11.22      11.11.11.22      0x8000001f   483  0x2  0xcf2   60
Router  *22.22.22.11      22.22.22.11      0x80000016  2276  0x22 0x27f7  84
Router   22.22.22.22      22.22.22.22      0x80000021   811  0x22 0x11c   96
Router   33.33.33.11      33.33.33.11      0x80000020  1058  0x22 0x1a6b  48
Router   33.33.33.22      33.33.33.22      0x8000001f  1261  0x22 0x411f  48
Network  10.0.0.1         11.11.11.11      0x80000018  1267  0x22 0xc1c9  32
Network  10.0.0.5         11.11.11.11      0x80000018  1023  0x22 0x8ce4  32
Network  10.0.0.9         11.11.11.11      0x80000018  1267  0x22 0xfe63  32
Network  10.0.0.13        11.11.11.22      0x8000001b   483  0x2  0xeb84  32
Network  10.0.0.18        22.22.22.22      0x8000001a  1231  0x22 0x3fe0  32
Network  10.0.0.22        22.22.22.22      0x8000001a   811  0x22 0xafb   32
Network  10.0.0.26        33.33.33.11      0x80000018  1058  0x22 0xb91e  32
Network  10.0.0.30        33.33.33.22      0x80000018  1261  0x22 0xbdff  32
Network  10.0.0.33        22.22.22.22      0x8000001a  1051  0x22 0x29b0  32
Network  10.0.0.37        22.22.22.22      0x8000001a  1051  0x22 0x9b2f  32
Network  10.0.0.42        22.22.22.22      0x8000001a  1231  0x22 0x4fcb  32
Summary  10.1.1.0         11.11.11.11      0x80000018  1267  0x22 0xda09  28
Summary  10.1.1.0         11.11.11.22      0x8000001e   795  0x2  0x5a34  28
Summary  192.168.41.1     11.11.11.11      0x80000018  1267  0x22 0xfd5d  28
Summary  192.168.41.1     11.11.11.22      0x8000001b   823  0x2  0x1ff3  28
Summary  192.168.42.1     11.11.11.11      0x80000018  1267  0x22 0x4d04  28
Summary  192.168.42.1     11.11.11.22      0x8000001c   795  0x2  0x6c9b  28
Summary  192.168.43.1     11.11.11.11      0x80000018  1267  0x22 0x420e  28
Summary  192.168.43.1     11.11.11.22      0x8000001c   798  0x2  0x61a5  28
Summary  192.168.44.1     11.11.11.11      0x80000018  1267  0x22 0xdc7b  28
Summary  192.168.44.1     11.11.11.22      0x8000001c   819  0x2  0xfb13  28
    OSPF AS SCOPE link state database
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len 
Extern   0.0.0.0          33.33.33.11      0x80000018  1308  0x20 0x2c81  36
Extern   0.0.0.0          33.33.33.22      0x80000018  1261  0x20 0xe9b8  36
Extern   10.10.10.0       11.11.11.11      0x80000018  1267  0x20 0x6f53  36
Extern   10.10.10.4       11.11.11.11      0x80000018  1267  0x20 0x4777  36
Extern   10.10.10.8       11.11.11.11      0x80000018  1267  0x20 0x1f9b  36
Extern   172.16.110.1     11.11.11.11      0x80000018  1267  0x20 0x9c15  36
Extern   172.16.210.1     11.11.11.11      0x80000018  1267  0x20 0x4c01  36
```

#### 3. ospf — borders — PASS
Command: `show ospf route abr instance VRF1`
```
 

Warning: License key missing; requires 'OSPF' license

Topology default Route Table:

Prefix             Path  Route      NH       Metric NextHop       Nexthop      
                   Type  Type       Type            Interface     Address/LSP
11.11.11.11        Intra Area/AS BR IP            1 et-0/0/4.0    10.0.0.5
11.11.11.22        Intra Area BR    IP            1 et-0/0/3.0    10.0.0.13
```

#### 4. ospf — config — PASS
Command: `show ospf overview instance VRF1`
```
 

Warning: License key missing; requires 'OSPF' license

Instance: VRF1
  Router ID: 22.22.22.11
  Route table index: 51
  LSA refresh time: 50 minutes
  Post Convergence Backup: Disabled
  DoNotAge uncapable
    Area scope LSAs received with no DC bit: 7
  Area: 0.0.0.0
    Stub type: Not Stub
    Authentication Type: None
    Area border routers: 2, AS boundary routers: 5
    Neighbors
      Up (in full state): 5
    DoNotAge uncapable
      Area scope LSAs received with no DC bit: 7
  Topology: default (ID 0)
    Prefix export count: 0
    Full SPF runs: 10
    SPF delay: 0.200000 sec, SPF holddown: 5 sec, SPF rapid runs: 3
    Backup SPF: Not Needed
```

#### 5. ospf — interfaces — PASS
Command: `show ospf interface instance VRF1`
```
 

Warning: License key missing; requires 'OSPF' license

Interface           State   Area            DR ID           BDR ID          Nbrs
et-0/0/0.0          BDR     0.0.0.0         33.33.33.11     22.22.22.11        1
et-0/0/1.0          BDR     0.0.0.0         33.33.33.22     22.22.22.11        1
et-0/0/2.0          BDR     0.0.0.0         22.22.22.22     22.22.22.11        1
et-0/0/3.0          BDR     0.0.0.0         11.11.11.22     22.22.22.11        1
et-0/0/4.0          BDR     0.0.0.0         11.11.11.11     22.22.22.11        1
```

#### 6. ospf — details — PASS
Command: `show ospf overview instance VRF1`
```
 

Warning: License key missing; requires 'OSPF' license

Instance: VRF1
  Router ID: 22.22.22.11
  Route table index: 51
  LSA refresh time: 50 minutes
  Post Convergence Backup: Disabled
  DoNotAge uncapable
    Area scope LSAs received with no DC bit: 7
  Area: 0.0.0.0
    Stub type: Not Stub
    Authentication Type: None
    Area border routers: 2, AS boundary routers: 5
    Neighbors
      Up (in full state): 5
    DoNotAge uncapable
      Area scope LSAs received with no DC bit: 7
  Topology: default (ID 0)
    Prefix export count: 0
    Full SPF runs: 10
    SPF delay: 0.200000 sec, SPF holddown: 5 sec, SPF rapid runs: 3
    Backup SPF: Not Needed
```

#### 7. routing_table — ip_route — PASS
Command: `show route instance VRF1`
```
 
Instance             Type
         Primary RIB                                     Active/holddown/hidden
VRF1                 virtual-router 
         VRF1.inet.0                                     29/0/0
```

#### 8. routing_table — route_maps — EMPTY
Command: `show configuration policy-options`
```
 
```

#### 9. routing_table — prefix_lists — EMPTY
Command: `show configuration policy-options`
```
 
```

#### 10. routing_table — policy_based_routing — PASS
Command: `show firewall filter`
```
 
missing mandatory argument: filtername.
```

#### 11. routing_table — access_lists — PASS
Command: `show firewall filter`
```
 
missing mandatory argument: filtername.
```

#### 12. interfaces — interface_status — PASS
Command: `show interfaces terse`
```
 
Interface               Admin Link Proto    Local                 Remote
et-0/0/0                up    up
et-0/0/0.0              up    up   inet     10.0.0.25/30    
                                   multiservice
pfh-0/0/0               up    up
pfh-0/0/0.16383         up    up   inet    
et-0/0/1                up    up
et-0/0/1.0              up    up   inet     10.0.0.29/30    
                                   multiservice
et-0/0/2                up    up
et-0/0/2.0              up    up   inet     10.0.0.21/30    
                                   multiservice
et-0/0/3                up    up
et-0/0/3.0              up    up   inet     10.0.0.14/30    
                                   multiservice
et-0/0/4                up    up
et-0/0/4.0              up    up   inet     10.0.0.6/30     
                                   multiservice
et-0/0/5                up    up
et-0/0/5.16386          up    up   multiservice
et-0/0/6                up    up
et-0/0/6.16386          up    up   multiservice
et-0/0/7                up    up
et-0/0/7.16386          up    up   multiservice
et-0/0/8                up    up
et-0/0/8.16386          up    up   multiservice
et-0/0/9                up    up
et-0/0/9.16386          up    up   multiservice
et-0/0/10               up    up
et-0/0/10.16386         up    up   multiservice
et-0/0/11               up    up
et-0/0/11.16386         up    up   multiservice
re0:mgmt-0              up    up
re0:mgmt-0.0            up    up   inet     172.20.20.207/24
dsc                     up    up
esi                     up    up
fti0                    up    up
fti1                    up    up
fti2                    up    up
fti3                    up    up
fti4                    up    up
fti5                    up    up
fti6                    up    up
fti7                    up    up
irb                     up    up
lbi                     up    up
lbi.0                   up    up   inet    
                                   inet6   
                                   mpls    
lo0                     up    up
lo0.0                   up    up   inet    
                                   inet6    fe80::a29:79f0:3b:374d-->  
lsi                     up    up
pip0                    up    up
vtep                    up    up
```

#### 13. tools — traceroute — PASS
Command: `traceroute routing-instance VRF1 172.20.20.207`
```
 
traceroute to 172.20.20.207 (172.20.20.207), 30 hops max, 60 byte packets
 1  10.0.0.30 (10.0.0.30)  2.764 ms  2.222 ms 10.0.0.26 (10.0.0.26)  1.733 ms
 2  * * *
 3  * * *
 4  * * *
 5  * * *
 6  * * *
 7  * * *
 8  * * *
 9  * * *
10  * * *
11  * * *
12  * * *
13  * * *
14  * * *
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```

### D2B — aruba_aoscx (aos)

#### 1. ospf — neighbors — PASS
Command: `show ip ospf neighbors`
```
VRF : default                          Process : 1
===================================================

Total Number of Neighbors : 7

Neighbor ID      Priority  State             Nbr Address       Interface
-------------------------------------------------------------------------
22.22.22.22      1         FULL/DR           10.0.0.18          1/1/6          

22.22.22.11      128       FULL/BDR          10.0.0.14          1/1/7          

11.11.11.11      1         FULL/DR           10.0.0.1           1/1/8          

1.1.1.1          128       FULL/DR           10.1.1.5           1/1/2          

2.2.2.2          1         FULL/DR           10.1.1.13          1/1/3          

3.3.3.3          1         FULL/DR           10.1.1.21          1/1/4          

4.4.4.4          128       FULL/DR           10.1.1.29          1/1/5          
```

#### 2. ospf — database — PASS
Command: `show ip ospf lsdb`
```
OSPF Router with ID (11.11.11.22) (Process ID 1 VRF default)
=============================================================

Router Link State Advertisements (Area 0.0.0.0)
------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum       Link Count
-------------------------------------------------------------------------------
9.9.9.9         9.9.9.9         1171      0x8000001c 0x00009d88     2
11.11.11.11     11.11.11.11     1024      0x80000022 0x0000a47c     3
11.11.11.22     11.11.11.22     483       0x8000001f 0x00000cf2     3
22.22.22.11     22.22.22.11     2281      0x80000016 0x000027f7     5
22.22.22.22     22.22.22.22     813       0x80000021 0x0000011c     6
33.33.33.11     33.33.33.11     1060      0x80000020 0x00001a6b     2
33.33.33.22     33.33.33.22     1264      0x8000001f 0x0000411f     2

Network Link State Advertisements (Area 0.0.0.0)
-------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
10.0.0.1        11.11.11.11     1270      0x80000018 0x0000c1c9
10.0.0.5        11.11.11.11     1024      0x80000018 0x00008ce4
10.0.0.9        11.11.11.11     1270      0x80000018 0x0000fe63
10.0.0.13       11.11.11.22     483       0x8000001b 0x0000eb84
10.0.0.18       22.22.22.22     1233      0x8000001a 0x00003fe0
10.0.0.22       22.22.22.22     813       0x8000001a 0x00000afb
10.0.0.26       33.33.33.11     1060      0x80000018 0x0000b91e
10.0.0.30       33.33.33.22     1264      0x80000018 0x0000bdff
10.0.0.33       22.22.22.22     1052      0x8000001a 0x000029b0
10.0.0.37       22.22.22.22     1052      0x8000001a 0x00009b2f
10.0.0.42       22.22.22.22     1233      0x8000001a 0x00004fcb

Inter-area Summary Link State Advertisements (Area 0.0.0.0)
------------------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
10.1.1.0        11.11.11.11     1270      0x80000018 0x0000da09
10.1.1.0        11.11.11.22     793       0x8000001e 0x00005a34
192.168.41.1    11.11.11.11     1270      0x80000018 0x0000fd5d
192.168.41.1    11.11.11.22     823       0x8000001b 0x00001ff3
192.168.42.1    11.11.11.11     1270      0x80000018 0x00004d04
192.168.42.1    11.11.11.22     793       0x8000001c 0x00006c9b
192.168.43.1    11.11.11.11     1270      0x80000018 0x0000420e
192.168.43.1    11.11.11.22     797       0x8000001c 0x000061a5
192.168.44.1    11.11.11.11     1270      0x80000018 0x0000dc7b
192.168.44.1    11.11.11.22     818       0x8000001c 0x0000fb13

Router Link State Advertisements (Area 0.0.0.1)
------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum       Link Count
-------------------------------------------------------------------------------
1.1.1.1         1.1.1.1         644       0x8000001f 0x000062da     3
2.2.2.2         2.2.2.2         1111      0x8000001d 0x0000ce0c     3
3.3.3.3         3.3.3.3         1112      0x8000001d 0x0000a30e     3
4.4.4.4         4.4.4.4         842       0x8000001f 0x0000a71a     3
11.11.11.11     11.11.11.11     1270      0x80000023 0x0000068e     4
11.11.11.22     11.11.11.22     788       0x80000021 0x0000e832     4

Network Link State Advertisements (Area 0.0.0.1)
-------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
10.1.1.2        11.11.11.11     1270      0x80000018 0x00002e8f
10.1.1.5        1.1.1.1         856       0x8000001b 0x000054a0
10.1.1.10       11.11.11.11     1270      0x80000018 0x000010a1
10.1.1.13       2.2.2.2         1111      0x8000001a 0x0000289d
10.1.1.18       11.11.11.11     1270      0x80000018 0x0000f1b3
10.1.1.21       3.3.3.3         1112      0x8000001a 0x0000dbd9
10.1.1.26       11.11.11.11     1270      0x80000018 0x0000d3c5
10.1.1.29       4.4.4.4         654       0x8000001b 0x00006f55

Inter-area Summary Link State Advertisements (Area 0.0.0.1)
------------------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
0.0.0.0         11.11.11.11     1270      0x80000018 0x000038c2
0.0.0.0         11.11.11.22     833       0x8000001b 0x0000d13b
10.0.0.0        11.11.11.11     1270      0x80000018 0x0000fdec
10.0.0.0        11.11.11.22     837       0x8000001b 0x00001f83
10.0.0.4        11.11.11.11     1270      0x80000018 0x0000d511
10.0.0.4        11.11.11.22     476       0x8000001c 0x0000fe9d
10.0.0.8        11.11.11.11     1270      0x80000018 0x0000ad35
10.0.0.8        11.11.11.22     828       0x8000001b 0x0000335d
10.0.0.12       11.11.11.11     1025      0x8000001a 0x00008b50
10.0.0.12       11.11.11.22     837       0x8000001b 0x0000a6ef
10.0.0.16       11.11.11.11     1270      0x80000018 0x0000c10f
10.0.0.16       11.11.11.22     838       0x8000001b 0x00007e14
10.0.0.20       11.11.11.11     1025      0x80000019 0x00003d97
10.0.0.20       11.11.11.22     476       0x8000001d 0x00005c2f
10.0.0.24       11.11.11.11     1025      0x80000019 0x000015bb
10.0.0.24       11.11.11.22     476       0x8000001c 0x00003652
10.0.0.28       11.11.11.11     1025      0x80000019 0x0000ecdf
10.0.0.28       11.11.11.22     476       0x8000001c 0x00000e76
10.0.0.32       11.11.11.11     1025      0x80000019 0x0000cef8
10.0.0.32       11.11.11.22     476       0x8000001d 0x0000ed90
... (19 more lines truncated)
```

#### 3. ospf — borders — PASS
Command: `show ip ospf border-routers`
```
VRF : default                          Process : 1
Internal Routing Table
---------------------------------------------------

Codes: i - Intra-area route, I - Inter-area route

           Router-ID   Cost  Type              Area     SPF           Nexthop                Interface
 i       11.11.11.11    101   ABR           0.0.0.1      38          10.1.1.5                    1/1/2
 i       11.11.11.11    101   ABR           0.0.0.1      38         10.1.1.29                    1/1/5
 i       11.11.11.11    100  BOTH           0.0.0.0      38          10.0.0.1                    1/1/8
 i           9.9.9.9    110  ASBR           0.0.0.0      38         10.0.0.18                    1/1/6
 i       22.22.22.22    100  ASBR           0.0.0.0      38         10.0.0.18                    1/1/6
 i       33.33.33.11    101  ASBR           0.0.0.0      38         10.0.0.14                    1/1/7
 i       33.33.33.22    101  ASBR           0.0.0.0      38         10.0.0.14                    1/1/7
```

#### 4. ospf — config — PASS
Command: `show ip ospf`
```
VRF : default                          Process  : 1
----------------------------------------------------

RouterID           : 11.11.11.22         OSPFv2                 : Enabled         
BFD                : Disabled            SPF Start Interval     : 200   ms
SPF Hold Interval  : 1000  ms            SPF Max Wait Interval  : 5000  ms
LSA Start Time     : 5000  ms            LSA Hold Time          : 0     ms
LSA Max Wait Time  : 0     ms            LSA Arrival            : 1000  ms
External LSAs      : 7                   Checksum Sum           : 185524              
ECMP               : 4                   Reference Bandwidth    : 100000 Mbps
Area Border        : true                AS Border              : false
GR Status          : Enabled             GR Interval            : 120
GR State           : inactive            GR Exit Status         : none            
GR Helper          : Disabled            GR Strict LSA Check    : Disabled        
GR Ignore Lost I/F : Disabled            
Summary address:

Area      Total     Active    
------------------------------
Normal     1         1
Stub       1         1
NSSA       0         0

Area  : 0.0.0.0
----------------
Area Type              : Normal         Status               : Active         
Total Interfaces       : 3              Active Interfaces    : 3              
Passive Interfaces     : 0              Loopback Interfaces  : 0
SPF Calculation Count  : 38             
Area ranges     : 
Number of LSAs         : 28             Checksum Sum         : 878902
Area  : 0.0.0.1
----------------
Area Type              : Stub           Status               : Active         
Total Interfaces       : 4              Active Interfaces    : 4              
Passive Interfaces     : 0              Loopback Interfaces  : 0
SPF Calculation Count  : 38             
Default Route Cost     : 1    
Area ranges     : 
    ip-prefix 10.1.1.0/24, inter-area, advertise
Number of LSAs         : 40             Checksum Sum         : 1469679
```

#### 5. ospf — interfaces — PASS
Command: `show ip ospf interface`
```
Codes: DR - Designated router  BDR - Backup Designated router

Interface 1/1/6 is up, line protocol is up
-------------------------------------------

VRF             : default                         Process             : 1
IP Address      : 10.0.0.17/30                    Area                : 0.0.0.0                         
Status          : up                              Network Type        : Broadcast                       
Hello Interval  : 10  sec                         Dead Interval       : 40  sec
Transit Delay   : 1   sec                         Retransmit Interval : 5   sec
Authentication  : No                              Link Speed          : 1000Mbps
Cost Configured : NA                              Cost Calculated     : 100
State/Type      : BDR                             Router Priority     : 1
DR              : 10.0.0.18                       BDR                 : 10.0.0.17
Link LSAs       : 0                               Checksum Sum        : 0    
BFD             : Disabled                        

Codes: DR - Designated router  BDR - Backup Designated router

Interface 1/1/7 is up, line protocol is up
-------------------------------------------

VRF             : default                         Process             : 1
IP Address      : 10.0.0.13/30                    Area                : 0.0.0.0                         
Status          : up                              Network Type        : Broadcast                       
Hello Interval  : 10  sec                         Dead Interval       : 40  sec
Transit Delay   : 1   sec                         Retransmit Interval : 5   sec
Authentication  : No                              Link Speed          : 1000Mbps
Cost Configured : NA                              Cost Calculated     : 100
State/Type      : DR                              Router Priority     : 1
DR              : 10.0.0.13                       BDR                 : 10.0.0.14
Link LSAs       : 0                               Checksum Sum        : 0    
BFD             : Disabled                        

Codes: DR - Designated router  BDR - Backup Designated router

Interface 1/1/8 is up, line protocol is up
-------------------------------------------

VRF             : default                         Process             : 1
IP Address      : 10.0.0.2/30                     Area                : 0.0.0.0                         
Status          : up                              Network Type        : Broadcast                       
Hello Interval  : 10  sec                         Dead Interval       : 40  sec
Transit Delay   : 1   sec                         Retransmit Interval : 5   sec
Authentication  : No                              Link Speed          : 1000Mbps
Cost Configured : NA                              Cost Calculated     : 100
State/Type      : BDR                             Router Priority     : 1
DR              : 10.0.0.1                        BDR                 : 10.0.0.2
Link LSAs       : 0                               Checksum Sum        : 0    
BFD             : Disabled                        

Codes: DR - Designated router  BDR - Backup Designated router

Interface 1/1/2 is up, line protocol is up
-------------------------------------------

VRF             : default                         Process             : 1
IP Address      : 10.1.1.6/30                     Area                : 0.0.0.1                         
Status          : up                              Network Type        : Broadcast                       
Hello Interval  : 10  sec                         Dead Interval       : 40  sec
Transit Delay   : 1   sec                         Retransmit Interval : 5   sec
Authentication  : No                              Link Speed          : 1000Mbps
Cost Configured : NA                              Cost Calculated     : 100
State/Type      : BDR                             Router Priority     : 1
DR              : 10.1.1.5                        BDR                 : 10.1.1.6
Link LSAs       : 0                               Checksum Sum        : 0    
BFD             : Disabled                        

Codes: DR - Designated router  BDR - Backup Designated router

Interface 1/1/3 is up, line protocol is up
-------------------------------------------

VRF             : default                         Process             : 1
IP Address      : 10.1.1.14/30                    Area                : 0.0.0.1                         
Status          : up                              Network Type        : Broadcast                       
Hello Interval  : 10  sec                         Dead Interval       : 40  sec
Transit Delay   : 1   sec                         Retransmit Interval : 5   sec
Authentication  : No                              Link Speed          : 1000Mbps
Cost Configured : NA                              Cost Calculated     : 100
State/Type      : BDR                             Router Priority     : 1
DR              : 10.1.1.13                       BDR                 : 10.1.1.14
Link LSAs       : 0                               Checksum Sum        : 0    
BFD             : Disabled                        

Codes: DR - Designated router  BDR - Backup Designated router

Interface 1/1/4 is up, line protocol is up
-------------------------------------------

VRF             : default                         Process             : 1
IP Address      : 10.1.1.22/30                    Area                : 0.0.0.1                         
Status          : up                              Network Type        : Broadcast                       
Hello Interval  : 10  sec                         Dead Interval       : 40  sec
Transit Delay   : 1   sec                         Retransmit Interval : 5   sec
Authentication  : No                              Link Speed          : 1000Mbps
Cost Configured : NA                              Cost Calculated     : 100
State/Type      : BDR                             Router Priority     : 1
DR              : 10.1.1.21                       BDR                 : 10.1.1.22
Link LSAs       : 0                               Checksum Sum        : 0    
... (18 more lines truncated)
```

#### 6. ospf — details — PASS
Command: `show ip ospf`
```
VRF : default                          Process  : 1
----------------------------------------------------

RouterID           : 11.11.11.22         OSPFv2                 : Enabled         
BFD                : Disabled            SPF Start Interval     : 200   ms
SPF Hold Interval  : 1000  ms            SPF Max Wait Interval  : 5000  ms
LSA Start Time     : 5000  ms            LSA Hold Time          : 0     ms
LSA Max Wait Time  : 0     ms            LSA Arrival            : 1000  ms
External LSAs      : 7                   Checksum Sum           : 185524              
ECMP               : 4                   Reference Bandwidth    : 100000 Mbps
Area Border        : true                AS Border              : false
GR Status          : Enabled             GR Interval            : 120
GR State           : inactive            GR Exit Status         : none            
GR Helper          : Disabled            GR Strict LSA Check    : Disabled        
GR Ignore Lost I/F : Disabled            
Summary address:

Area      Total     Active    
------------------------------
Normal     1         1
Stub       1         1
NSSA       0         0

Area  : 0.0.0.0
----------------
Area Type              : Normal         Status               : Active         
Total Interfaces       : 3              Active Interfaces    : 3              
Passive Interfaces     : 0              Loopback Interfaces  : 0
SPF Calculation Count  : 38             
Area ranges     : 
Number of LSAs         : 28             Checksum Sum         : 878902
Area  : 0.0.0.1
----------------
Area Type              : Stub           Status               : Active         
Total Interfaces       : 4              Active Interfaces    : 4              
Passive Interfaces     : 0              Loopback Interfaces  : 0
SPF Calculation Count  : 38             
Default Route Cost     : 1    
Area ranges     : 
    ip-prefix 10.1.1.0/24, inter-area, advertise
Number of LSAs         : 40             Checksum Sum         : 1469679
```

#### 7. routing_table — ip_route — PASS
Command: `show ip route`
```
Displaying ipv4 routes selected for forwarding

Origin Codes: C - connected, S - static, L - local
              R - RIP, B - BGP, O - OSPF
Type Codes:   E - External BGP, I - Internal BGP, V - VPN, EV - EVPN
              IA - OSPF internal area, E1 - OSPF external type 1
              E2 - OSPF external type 2

VRF: default

Prefix              Nexthop          Interface     VRF(egress)       Origin/   Distance/    Age
                                                                     Type      Metric
---------------------------------------------------------------------------------------------------------
0.0.0.0/0           10.0.0.14        1/1/7         -                 O/E1      [110/102]    13h:08m:34s  
10.0.0.0/30         -                1/1/8         -                 C         [0/0]        -            
10.0.0.2/32         -                1/1/8         -                 L         [0/0]        -            
10.0.0.4/30         10.0.0.14        1/1/7         -                 O         [110/101]    13h:08m:34s  
10.0.0.8/30         10.0.0.18        1/1/6         -                 O         [110/110]    13h:14m:17s  
                    10.0.0.1         1/1/8         -                           [110/110]    13h:14m:17s  
10.0.0.12/30        -                1/1/7         -                 C         [0/0]        -            
10.0.0.13/32        -                1/1/7         -                 L         [0/0]        -            
10.0.0.16/30        -                1/1/6         -                 C         [0/0]        -            
10.0.0.17/32        -                1/1/6         -                 L         [0/0]        -            
10.0.0.20/30        10.0.0.14        1/1/7         -                 O         [110/101]    13h:08m:34s  
10.0.0.24/30        10.0.0.14        1/1/7         -                 O         [110/101]    13h:08m:34s  
10.0.0.28/30        10.0.0.14        1/1/7         -                 O         [110/101]    13h:08m:34s  
10.0.0.32/30        10.0.0.14        1/1/7         -                 O         [110/102]    13h:08m:34s  
10.0.0.36/30        10.0.0.14        1/1/7         -                 O         [110/102]    13h:08m:34s  
10.0.0.40/30        10.0.0.18        1/1/6         -                 O         [110/110]    13h:14m:17s  
10.1.1.0/24         -                reject        -                 S         [110/0]      13h:14m:19s  
10.1.1.0/30         10.1.1.5         1/1/2         -                 O         [110/101]    13h:14m:19s  
10.1.1.4/30         -                1/1/2         -                 C         [0/0]        -            
10.1.1.6/32         -                1/1/2         -                 L         [0/0]        -            
10.1.1.8/30         10.1.1.13        1/1/3         -                 O         [110/110]    13h:13m:52s  
10.1.1.12/30        -                1/1/3         -                 C         [0/0]        -            
10.1.1.14/32        -                1/1/3         -                 L         [0/0]        -            
10.1.1.16/30        10.1.1.21        1/1/4         -                 O         [110/110]    13h:13m:56s  
10.1.1.20/30        -                1/1/4         -                 C         [0/0]        -            
10.1.1.22/32        -                1/1/4         -                 L         [0/0]        -            
10.1.1.24/30        10.1.1.29        1/1/5         -                 O         [110/101]    13h:14m:17s  
10.1.1.28/30        -                1/1/5         -                 C         [0/0]        -            
10.1.1.30/32        -                1/1/5         -                 L         [0/0]        -            
10.9.9.1/32         10.0.0.18        1/1/6         -                 O         [110/120]    13h:14m:17s  
10.10.10.0/30       10.1.1.5         1/1/2         -                 O/E1      [110/121]    13h:14m:17s  
                    10.1.1.29        1/1/5         -                           [110/121]    13h:14m:17s  
10.10.10.4/30       10.1.1.5         1/1/2         -                 O/E1      [110/121]    13h:14m:17s  
                    10.1.1.29        1/1/5         -                           [110/121]    13h:14m:17s  
10.10.10.8/30       10.1.1.5         1/1/2         -                 O/E1      [110/121]    13h:14m:17s  
                    10.1.1.29        1/1/5         -                           [110/121]    13h:14m:17s  
172.16.110.1/32     10.1.1.5         1/1/2         -                 O/E1      [110/121]    13h:14m:17s  
                    10.1.1.29        1/1/5         -                           [110/121]    13h:14m:17s  
172.16.210.1/32     10.1.1.5         1/1/2         -                 O/E1      [110/121]    13h:14m:17s  
                    10.1.1.29        1/1/5         -                           [110/121]    13h:14m:17s  
192.168.41.1/32     10.1.1.5         1/1/2         -                 O         [110/101]    13h:14m:19s  
192.168.42.1/32     10.1.1.13        1/1/3         -                 O         [110/110]    13h:13m:52s  
192.168.43.1/32     10.1.1.21        1/1/4         -                 O         [110/110]    13h:13m:56s  
192.168.44.1/32     10.1.1.29        1/1/5         -                 O         [110/101]    13h:14m:17s  

Total Route Count : 38
```

#### 8. routing_table — route_maps — EMPTY
Command: `show route-map`
```

```

#### 9. routing_table — prefix_lists — EMPTY
Command: `show ip prefix-list`
```

```

#### 10. routing_table — policy_based_routing — PASS
Command: `show policy`
```
No Policy found.
```

#### 11. routing_table — access_lists — PASS
Command: `show access-list`
```
No ACL found.
```

#### 12. interfaces — interface_status — PASS
Command: `show interface brief`
```
--------------------------------------------------------------------------------------------------------------
Port      Native  Mode   Type           Enabled Status  Reason                 Speed   Description
          VLAN                                                                 (Mb/s)  
--------------------------------------------------------------------------------------------------------------
1/1/1     --      routed --             no      down    Administratively down  --      --
1/1/2     --      routed --             yes     up                             1000    TO-A1M
1/1/3     --      routed --             yes     up                             1000    TO-A2V
1/1/4     --      routed --             yes     up                             1000    TO-A3V
1/1/5     --      routed --             yes     up                             1000    TO-A4M
1/1/6     --      routed --             yes     up                             1000    TO-C2A
1/1/7     --      routed --             yes     up                             1000    TO-C1J
1/1/8     --      routed --             yes     up                             1000    TO-D1C
1/1/9     --      routed --             no      down    Administratively down  --      --
1/1/10    --      routed --             no      down    Administratively down  --      --
1/1/11    --      routed --             no      down    No XCVR installed      --      --
1/1/12    --      routed --             no      down    No XCVR installed      --      --
1/1/13    --      routed --             no      down    No XCVR installed      --      --
1/1/14    --      routed --             no      down    No XCVR installed      --      --
1/1/15    --      routed --             no      down    No XCVR installed      --      --
1/1/16    --      routed --             no      down    No XCVR installed      --      --
1/1/17    --      routed --             no      down    No XCVR installed      --      --
1/1/18    --      routed --             no      down    No XCVR installed      --      --
1/1/19    --      routed --             no      down    No XCVR installed      --      --
1/1/20    --      routed --             no      down    No XCVR installed      --      --
1/1/21    --      routed --             no      down    No XCVR installed      --      --
1/1/22    --      routed --             no      down    No XCVR installed      --      --
1/1/23    --      routed --             no      down    No XCVR installed      --      --
1/1/24    --      routed --             no      down    No XCVR installed      --      --
1/1/25    --      routed --             no      down    No XCVR installed      --      --
1/1/26    --      routed --             no      down    No XCVR installed      --      --
1/1/27    --      routed --             no      down    No XCVR installed      --      --
1/1/28    --      routed --             no      down    No XCVR installed      --      --
1/1/29    --      routed --             no      down    No XCVR installed      --      --
1/1/30    --      routed --             no      down    No XCVR installed      --      --
1/1/31    --      routed --             no      down    No XCVR installed      --      --
1/1/32    --      routed --             no      down    No XCVR installed      --      --
1/1/33    --      routed --             no      down    No XCVR installed      --      --
1/1/34    --      routed --             no      down    No XCVR installed      --      --
1/1/35    --      routed --             no      down    No XCVR installed      --      --
1/1/36    --      routed --             no      down    No XCVR installed      --      --
1/1/37    --      routed --             no      down    No XCVR installed      --      --
1/1/38    --      routed --             no      down    No XCVR installed      --      --
1/1/39    --      routed --             no      down    No XCVR installed      --      --
1/1/40    --      routed --             no      down    No XCVR installed      --      --
1/1/41    --      routed --             no      down    No XCVR installed      --      --
1/1/42    --      routed --             no      down    No XCVR installed      --      --
1/1/43    --      routed --             no      down    No XCVR installed      --      --
1/1/44    --      routed --             no      down    No XCVR installed      --      --
1/1/45    --      routed --             no      down    No XCVR installed      --      --
1/1/46    --      routed --             no      down    No XCVR installed      --      --
1/1/47    --      routed --             no      down    No XCVR installed      --      --
1/1/48    --      routed --             no      down    No XCVR installed      --      --
1/1/49    --      routed --             no      down    No XCVR installed      --      --
1/1/50    --      routed --             no      down    No XCVR installed      --      --
1/1/51    --      routed --             no      down    No XCVR installed      --      --
1/1/52    --      routed --             no      down    No XCVR installed      --      --
```

#### 13. tools — traceroute — PASS
Command: `traceroute 172.20.20.207 probes 1 timeout 2`
```
traceroute to 172.20.20.207 (172.20.20.207), 1 hops min, 30 hops max, 2 sec. timeout, 1 probes
  1   10.0.0.14  3.565ms 
  2   10.0.0.26  3.168ms 
  3   * 
  4   * 
  5   * 
  6   * 
  7   * 
  8   * 
  9   * 
 10   * 
 11   * 
 12   * 
 13   * 
 14   * 
 15   * 
 16   * 
 17   * 
 18   * 
 19   * 
 20   * 
 21   * 
 22   * 
 23   * 
 24   * 
 25   * 
 26   * 
 27   * 
 28   * 
 29   * 
 30   * 
```

### A1M — mikrotik_routeros (routeros)

#### 1. ospf — neighbors — PASS
Command: `/routing ospf neighbor print terse without-paging`
```
0 D instance=default area=area1 address=10.1.1.2 priority=1 router-id=11.11.11.11 dr=10.1.1.2 bdr=10.1.1.1 state=Full state-changes=6 adjacency=13h14m35s timeout=31s
1 D instance=default area=area1 address=10.1.1.6 priority=1 router-id=11.11.11.22 dr=10.1.1.5 bdr=10.1.1.6 state=Full state-changes=6 adjacency=13h13m43s timeout=38s




 




[admin@A1M] > 
```

#### 2. ospf — database — PASS
Command: `/routing ospf lsa print without-paging`
```
Flags: S - self-originated, F - flushing, W - wraparound; D - dynamic 
 0 SD instance=default area=area1 type="router" originator=1.1.1.1 id=1.1.1.1 
      sequence=0x8000001F age=638 checksum=0x62DA body=
        options=
            type=network id=10.1.1.2 data=10.1.1.1 metric=1
            type=network id=10.1.1.5 data=10.1.1.5 metric=1
            type=stub id=192.168.41.1 data=255.255.255.255 metric=1

 1  D instance=default area=area1 type="router" originator=2.2.2.2 id=2.2.2.2 
      sequence=0x8000001D age=1113 checksum=0xCE0C body=
        options=DC
            type=stub id=192.168.42.1 data=255.255.255.255 metric=10
            type=network id=10.1.1.13 data=10.1.1.13 metric=10
            type=network id=10.1.1.10 data=10.1.1.9 metric=10

 2  D instance=default area=area1 type="router" originator=3.3.3.3 id=3.3.3.3 
      sequence=0x8000001D age=1114 checksum=0xA30E body=
        options=DC
            type=stub id=192.168.43.1 data=255.255.255.255 metric=10
            type=network id=10.1.1.18 data=10.1.1.17 metric=10
            type=network id=10.1.1.21 data=10.1.1.21 metric=10

 3  D instance=default area=area1 type="router" originator=4.4.4.4 id=4.4.4.4 
      sequence=0x8000001F age=844 checksum=0xA71A body=
        options=
            type=network id=10.1.1.26 data=10.1.1.25 metric=1
            type=network id=10.1.1.29 data=10.1.1.29 metric=1
            type=stub id=192.168.44.1 data=255.255.255.255 metric=1

 4  D instance=default area=area1 type="router" originator=11.11.11.11 
      id=11.11.11.11 sequence=0x80000023 age=1270 checksum=0x68E 
      body=
        options=DC bits=B
            type=network id=10.1.1.26 data=10.1.1.26 metric=10
            type=network id=10.1.1.18 data=10.1.1.18 metric=10
            type=network id=10.1.1.10 data=10.1.1.10 metric=10
            type=network id=10.1.1.2 data=10.1.1.2 metric=10

 5  D instance=default area=area1 type="router" originator=11.11.11.22 
      id=11.11.11.22 sequence=0x80000021 age=790 checksum=0xE832 
      body=
        options= bits=B
            type=network id=10.1.1.5 data=10.1.1.6 metric=100
            type=network id=10.1.1.13 data=10.1.1.14 metric=100
            type=network id=10.1.1.21 data=10.1.1.22 metric=100
            type=network id=10.1.1.29 data=10.1.1.30 metric=100

 6  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.2 sequence=0x80000018 age=1270 checksum=0x2E8F 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=1.1.1.1

 7 SD instance=default area=area1 type="network" originator=1.1.1.1 id=10.1.1.5
      sequence=0x8000001B age=850 checksum=0x54A0 body=
        netmask=255.255.255.252
            router-id=1.1.1.1
            router-id=11.11.11.22

 8  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.10 sequence=0x80000018 age=1270 checksum=0x10A1 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=2.2.2.2

 9  D instance=default area=area1 type="network" originator=2.2.2.2 
      id=10.1.1.13 sequence=0x8000001A age=1113 checksum=0x289D 
      body=
        netmask=255.255.255.252
            router-id=2.2.2.2
            router-id=11.11.11.22

10  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.18 sequence=0x80000018 age=1270 checksum=0xF1B3 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=3.3.3.3

11  D instance=default area=area1 type="network" originator=3.3.3.3 
      id=10.1.1.21 sequence=0x8000001A age=1114 checksum=0xDBD9 
      body=
        netmask=255.255.255.252
            router-id=3.3.3.3
            router-id=11.11.11.22

12  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.26 sequence=0x80000018 age=1270 checksum=0xD3C5 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=4.4.4.4

13  D instance=default area=area1 type="network" originator=4.4.4.4 
      id=10.1.1.29 sequence=0x8000001B age=656 checksum=0x6F55 
      body=
        netmask=255.255.255.252
            router-id=4.4.4.4
... (167 more lines truncated)
```

#### 3. ospf — borders — PASS
Command: `/routing ospf instance print without-paging`
```
Flags: X - disabled, I - inactive 
 0   name="default" version=2 vrf=VRF1 router-id=1.1.1.1 




 




[admin@A1M] > 
```

#### 4. ospf — config — PASS
Command: `/routing ospf area print detail without-paging`
```
Flags: X - disabled, I - inactive, D - dynamic; T - transit-capable 
 0    name="area1" instance=default area-id=0.0.0.1 type=stub 




 




[admin@A1M] > 
```

#### 5. ospf — interfaces — PASS
Command: `/routing ospf interface print terse without-paging`
```
0 D address=10.1.1.1%ether2 area=area1 state=bdr network-type=broadcast dr=10.1.1.2 cost=1 priority=128 use-bfd=no retransmit-interval=5s transmit-delay=1s hello-interval=10s dead-interval=40s
1 D address=10.1.1.5%ether3 area=area1 state=dr network-type=broadcast bdr=10.1.1.6 cost=1 priority=128 use-bfd=no retransmit-interval=5s transmit-delay=1s hello-interval=10s dead-interval=40s
2 D address=192.168.41.1%lo0 area=area1 state=passive network-type=broadcast cost=1 priority=128 use-bfd=no retransmit-interval=5s transmit-delay=1s hello-interval=10s dead-interval=40s




 




[admin@A1M] > 
```

#### 6. ospf — details — PASS
Command: `/routing ospf instance print detail without-paging`
```
Flags: X - disabled, I - inactive 
 0   name="default" version=2 vrf=VRF1 router-id=1.1.1.1 




 




[admin@A1M] > 
```

#### 7. routing_table — ip_route — PASS
Command: `/ip route print without-paging`
```
Flags: D - DYNAMIC; A - ACTIVE; c - CONNECT, s - STATIC, o - OSPF; + - ECMP
Columns: DST-ADDRESS, GATEWAY, ROUTING-TABLE, DISTANCE
#      DST-ADDRESS       GATEWAY               ROUTING-TABLE  DISTANCE
0  As  172.20.20.0/24    172.31.255.29         main                  1
  DAc  172.31.255.28/30  ether1                main                  0
  DAo+ 0.0.0.0/0         10.1.1.6%ether3@VRF1  VRF1                110
  DAo+ 0.0.0.0/0         10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.0.0.0/30       10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.0.0.4/30       10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.0.0.8/30       10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.0.0.12/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.0.0.16/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.0.0.20/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.0.0.24/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.0.0.28/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.0.0.32/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.0.0.36/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.0.0.40/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAc  10.1.1.0/30       ether2@VRF1           VRF1                  0
  DAc  10.1.1.4/30       ether3@VRF1           VRF1                  0
  DAo  10.1.1.8/30       10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.1.1.12/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.1.1.16/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.1.1.20/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.1.1.24/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.1.1.28/30      10.1.1.2%ether2@VRF1  VRF1                110
  DAo  10.9.9.1/32       10.1.1.2%ether2@VRF1  VRF1                110
  DAc  192.168.41.1/32   lo0@VRF1              VRF1                  0
  DAo  192.168.42.1/32   10.1.1.2%ether2@VRF1  VRF1                110
  DAo  192.168.43.1/32   10.1.1.2%ether2@VRF1  VRF1                110
  DAo  192.168.44.1/32   10.1.1.2%ether2@VRF1  VRF1                110




 




[admin@A1M] > 
```

#### 8. routing_table — route_maps — PASS
Command: `/routing filter print without-paging`
```
bad command name print (line 1 column 17)



 




[admin@A1M] > 
```

#### 9. routing_table — prefix_lists — PASS
Command: `/routing filter print without-paging`
```
bad command name print (line 1 column 17)



 




[admin@A1M] > 
```

#### 10. routing_table — policy_based_routing — PASS
Command: `/ip firewall mangle print without-paging`
```
Flags: X - disabled, I - invalid; D - dynamic 




 




[admin@A1M] > 
```

#### 11. routing_table — access_lists — PASS
Command: `/ip firewall filter print without-paging`
```
Flags: X - disabled, I - invalid; D - dynamic 




 




[admin@A1M] > 
```

#### 12. interfaces — interface_status — PASS
Command: `/interface print brief without-paging`
```
Flags: R - RUNNING
Columns: NAME, TYPE, ACTUAL-MTU, L2MTU, MAC-ADDRESS
#   NAME    TYPE      ACTUAL-MTU  L2MTU  MAC-ADDRESS      
0 R ether1  ether           1500         0C:00:35:D6:17:00
;;; TO-D1C
1 R ether2  ether           1500         AA:C1:AB:EE:89:AF
;;; TO-D2B
2 R ether3  ether           1500         AA:C1:AB:D2:43:53
3 R VRF1    vrf            65536         36:7A:13:01:09:45
4 R lo      loopback       65536         00:00:00:00:00:00
;;; Loopback0
5 R lo0     bridge          1500  65535  56:2C:EA:8F:80:BC




 




[admin@A1M] > 
```

#### 13. tools — traceroute — PASS
Command: `/tool/traceroute count=1 address=172.20.20.207`
```
ADDRESS                          LOSS SENT    LAST     AVG    BEST   WORST
172.31.255.29                      0%    1   0.1ms     0.1     0.1     0.1
172.20.20.207                      0%    1   0.5ms     0.5     0.5     0.5




 




[admin@A1M] > 
```
