# Platform Coverage Results
*Generated: 2026-03-28 16:04:54 UTC*

## Summary

| Device | Platform | CLI Style | Tests | Passed | Empty | Failed |
|--------|----------|-----------|-------|--------|-------|--------|
| D1C | cisco_iosxe | ios | 7 | 7 | 0 | 0 |
| A2A | arista_eos | eos | 7 | 7 | 0 | 0 |
| C1J | juniper_junos | junos | 7 | 7 | 0 | 0 |
| D2B | aruba_aoscx | aos | 7 | 7 | 0 | 0 |
| A1M | mikrotik_routeros | routeros | 7 | 7 | 0 | 0 |
| **Total** | | | **35** | **35** | **0** | **0** |

## Detailed Results

### D1C — cisco_iosxe (ios)

#### 1. ospf — neighbors — PASS
Command: `show ip ospf neighbor`
```
Neighbor ID     Pri   State           Dead Time   Address         Interface
22.22.22.22       1   FULL/BDR        00:00:30    10.0.0.10       Ethernet1/2
22.22.22.11     128   FULL/BDR        00:00:39    10.0.0.6        Ethernet1/3
11.11.11.22       1   FULL/BDR        00:00:32    10.0.0.2        Ethernet1/1
4.4.4.4         128   FULL/BDR        00:00:31    10.1.1.25       Ethernet1/0
3.3.3.3           1   FULL/BDR        00:00:30    10.1.1.17       Ethernet0/3
2.2.2.2           1   FULL/BDR        00:00:39    10.1.1.9        Ethernet0/2
1.1.1.1         128   FULL/BDR        00:00:31    10.1.1.1        Ethernet0/1
```

#### 2. ospf — database — PASS
Command: `show ip ospf database`
```
            OSPF Router with ID (11.11.11.11) (Process ID 1)

		Router Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum Link count
9.9.9.9         9.9.9.9         1838        0x80000016 0x00A982 2         
11.11.11.11     11.11.11.11     574         0x8000001D 0x00AE77 3         
11.11.11.22     11.11.11.22     792         0x80000019 0x0018EC 3         
22.22.22.11     22.22.22.11     788         0x80000013 0x002DF4 5         
22.22.22.22     22.22.22.22     1480        0x8000001B 0x000D16 6         
33.33.33.11     33.33.33.11     584         0x8000001B 0x002466 2         
33.33.33.22     33.33.33.22     840         0x8000001A 0x004B1A 2         

		Net Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum
10.0.0.1        11.11.11.11     820         0x80000013 0x00CBC4
10.0.0.5        11.11.11.11     574         0x80000013 0x0096DF
10.0.0.9        11.11.11.11     820         0x80000013 0x00095E
10.0.0.13       11.11.11.22     792         0x80000015 0x00F77E
10.0.0.18       22.22.22.22     40          0x80000015 0x0049DB
10.0.0.22       22.22.22.22     1480        0x80000014 0x0016F5
10.0.0.26       33.33.33.11     584         0x80000013 0x00C319
10.0.0.30       33.33.33.22     840         0x80000013 0x00C7FA
10.0.0.33       22.22.22.22     1720        0x80000014 0x0035AA
10.0.0.37       22.22.22.22     1720        0x80000014 0x00A729
10.0.0.42       22.22.22.22     40          0x80000015 0x0059C6

		Summary Net Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum
10.1.1.0        11.11.11.11     820         0x80000013 0x00E404
10.1.1.0        11.11.11.22     1102        0x80000018 0x00662E
192.168.41.1    11.11.11.11     820         0x80000013 0x000858
192.168.41.1    11.11.11.22     1132        0x80000015 0x002BED
192.168.42.1    11.11.11.11     820         0x80000013 0x0057FE
192.168.42.1    11.11.11.22     1102        0x80000016 0x007895
192.168.43.1    11.11.11.11     820         0x80000013 0x004C09
192.168.43.1    11.11.11.22     1106        0x80000016 0x006D9F
192.168.44.1    11.11.11.11     820         0x80000013 0x00E676
192.168.44.1    11.11.11.22     1127        0x80000016 0x00080D

		Router Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum Link count
1.1.1.1         1.1.1.1         950         0x80000019 0x006ED4 3         
2.2.2.2         2.2.2.2         1778        0x80000017 0x00DA06 3         
3.3.3.3         3.3.3.3         1779        0x80000017 0x00AF08 3         
4.4.4.4         4.4.4.4         1204        0x80000019 0x00B314 3         
11.11.11.11     11.11.11.11     820         0x8000001E 0x001089 4         
11.11.11.22     11.11.11.22     1098        0x8000001B 0x00F42C 4         

		Net Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum
10.1.1.2        11.11.11.11     820         0x80000013 0x00388A
10.1.1.5        1.1.1.1         1173        0x80000015 0x00609A
10.1.1.10       11.11.11.11     820         0x80000013 0x001A9C
10.1.1.13       2.2.2.2         1778        0x80000014 0x003497
10.1.1.18       11.11.11.11     820         0x80000013 0x00FBAE
10.1.1.21       3.3.3.3         1779        0x80000014 0x00E7D3
10.1.1.26       11.11.11.11     820         0x80000013 0x00DDC0
10.1.1.29       4.4.4.4         909         0x80000015 0x007B4F

		Summary Net Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum
0.0.0.0         11.11.11.11     820         0x80000013 0x0042BD
0.0.0.0         11.11.11.22     1143        0x80000015 0x00DD35
10.0.0.0        11.11.11.11     820         0x80000013 0x0008E7
10.0.0.0        11.11.11.22     1147        0x80000015 0x002B7D
10.0.0.4        11.11.11.11     820         0x80000013 0x00DF0C
10.0.0.4        11.11.11.22     786         0x80000016 0x000B97
10.0.0.8        11.11.11.11     820         0x80000013 0x00B730
10.0.0.8        11.11.11.22     1138        0x80000015 0x003F57
10.0.0.12       11.11.11.11     574         0x80000015 0x00954B
10.0.0.12       11.11.11.22     1147        0x80000015 0x00B2E9
10.0.0.16       11.11.11.11     820         0x80000013 0x00CB0A
10.0.0.16       11.11.11.22     1148        0x80000015 0x008A0E
10.0.0.20       11.11.11.11     574         0x80000014 0x004792
10.0.0.20       11.11.11.22     786         0x80000017 0x006829
10.0.0.24       11.11.11.11     574         0x80000014 0x001FB6
10.0.0.24       11.11.11.22     786         0x80000016 0x00424C
10.0.0.28       11.11.11.11     574         0x80000014 0x00F6DA
10.0.0.28       11.11.11.22     786         0x80000016 0x001A70
10.0.0.32       11.11.11.11     574         0x80000014 0x00D8F3
10.0.0.32       11.11.11.22     786         0x80000017 0x00F98A
10.0.0.36       11.11.11.11     574         0x80000014 0x00B018
10.0.0.36       11.11.11.22     786         0x80000017 0x00D1AE
10.0.0.40       11.11.11.11     820         0x80000013 0x00DAE2
10.0.0.40       11.11.11.22     1128        0x80000016 0x00FB79
10.9.9.1        11.11.11.11     820         0x80000013 0x0009BC
10.9.9.1        11.11.11.22     1128        0x80000015 0x002C52

		Type-5 AS External Link States

Link ID         ADV Router      Age         Seq#       Checksum Tag
0.0.0.0         33.33.33.11     845         0x80000013 0x00367C 1         
0.0.0.0         33.33.33.22     840         0x80000013 0x00F3B3 1         
10.10.10.0      11.11.11.11     820         0x80000013 0x00794E 0         
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
    Hello due in 00:00:03
  Supports Link-local Signaling (LLS)
  Cisco NSF helper support enabled
  IETF NSF helper support enabled
  Can be protected by per-prefix Loop-Free FastReroute
  Can be used for per-prefix Loop-Free FastReroute repair paths
  Not Protected by per-prefix TI-LFA
  Index 1/3/3, flood queue length 0
  Next 0x0(0)/0x0(0)/0x0(0)
  Last flood scan length is 0, maximum is 12
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
    Hello due in 00:00:02
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
  Last flood scan length is 2, maximum is 12
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
    Hello due in 00:00:08
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
 Start time: 00:00:02.388, Time elapsed: 10:21:06.894
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
 Number of external LSA 7. Checksum Sum 0x031B90
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
	SPF algorithm last executed 10:13:33.620 ago
	SPF algorithm executed 32 times
	Area ranges are
	Number of LSA 28. Checksum Sum 0x0B96A0
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
	SPF algorithm last executed 10:18:51.316 ago
	SPF algorithm executed 20 times
	Area ranges are
	   10.1.1.0/24 Active(10) Advertise 
	Number of LSA 40. Checksum Sum 0x152B11
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

#### 7. interfaces — interface_status — PASS
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

### A2A — arista_eos (eos)

#### 1. ospf — neighbors — PASS
Command: `show ip ospf neighbor vrf VRF1`
```
Neighbor ID     Instance VRF      Pri State                  Dead Time   Address         Interface
11.11.11.22     1        VRF1     1   FULL/BDR               00:00:29    10.1.1.14       Ethernet2
11.11.11.11     1        VRF1     1   FULL/DR                00:00:36    10.1.1.10       Ethernet1
```

#### 2. ospf — database — PASS
Command: `show ip ospf database vrf VRF1`
```
            OSPF Router with ID(2.2.2.2) (Instance ID 1) (VRF VRF1)


                 Router Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#         Checksum Link count
3.3.3.3         3.3.3.3         1782        0x80000017   0xaf08   3
4.4.4.4         4.4.4.4         1207        0x80000019   0xb314   3
2.2.2.2         2.2.2.2         1779        0x80000017   0xda06   3
1.1.1.1         1.1.1.1         953         0x80000019   0x6ed4   3
11.11.11.11     11.11.11.11     824         0x8000001e   0x1089   4
11.11.11.22     11.11.11.22     1099        0x8000001b   0xf42c   4

                 Network Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#         Checksum
10.1.1.5        1.1.1.1         1176        0x80000015   0x609a  
10.1.1.26       11.11.11.11     824         0x80000013   0xddc0  
10.1.1.2        11.11.11.11     824         0x80000013   0x388a  
10.1.1.18       11.11.11.11     824         0x80000013   0xfbae  
10.1.1.10       11.11.11.11     824         0x80000013   0x1a9c  
10.1.1.29       4.4.4.4         912         0x80000015   0x7b4f  
10.1.1.21       3.3.3.3         1782        0x80000014   0xe7d3  
10.1.1.13       2.2.2.2         1779        0x80000014   0x3497  

                 Summary Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#         Checksum
10.0.0.4        11.11.11.11     824         0x80000013   0xdf0c  
0.0.0.0         11.11.11.22     1144        0x80000015   0xdd35  
0.0.0.0         11.11.11.11     824         0x80000013   0x42bd  
10.9.9.1        11.11.11.11     824         0x80000013   0x9bc   
10.0.0.8        11.11.11.11     824         0x80000013   0xb730  
10.0.0.16       11.11.11.11     824         0x80000013   0xcb0a  
10.0.0.32       11.11.11.11     577         0x80000014   0xd8f3  
10.0.0.0        11.11.11.11     824         0x80000013   0x8e7   
10.0.0.0        11.11.11.22     1148        0x80000015   0x2b7d  
10.0.0.32       11.11.11.22     787         0x80000017   0xf98a  
10.0.0.16       11.11.11.22     1149        0x80000015   0x8a0e  
10.0.0.24       11.11.11.11     577         0x80000014   0x1fb6  
10.0.0.40       11.11.11.11     824         0x80000013   0xdae2  
10.0.0.8        11.11.11.22     1139        0x80000015   0x3f57  
10.0.0.40       11.11.11.22     1131        0x80000016   0xfb79  
10.0.0.24       11.11.11.22     787         0x80000016   0x424c  
10.0.0.12       11.11.11.22     1148        0x80000015   0xb2e9  
10.0.0.20       11.11.11.11     577         0x80000014   0x4792  
10.0.0.36       11.11.11.11     577         0x80000014   0xb018  
10.0.0.4        11.11.11.22     787         0x80000016   0xb97   
10.0.0.36       11.11.11.22     787         0x80000017   0xd1ae  
10.0.0.20       11.11.11.22     787         0x80000017   0x6829  
10.0.0.28       11.11.11.11     577         0x80000014   0xf6da  
10.0.0.12       11.11.11.11     577         0x80000015   0x954b  
10.0.0.28       11.11.11.22     787         0x80000016   0x1a70  
10.9.9.1        11.11.11.22     1131        0x80000015   0x2c52  
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
 Time since last SPF 36816 secs
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
   Number of LSA 40. Checksum Sum 1387281
   Number of opaque link LSA 0. Checksum Sum 0
   Number of opaque area LSA 0. Checksum Sum 0
   Number of indication LSA 0
   Number of DC-clear LSA 18
```

#### 7. interfaces — interface_status — PASS
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

### C1J — juniper_junos (junos)

#### 1. ospf — neighbors — PASS
Command: `show ospf neighbor instance VRF1`
```
 

Warning: License key missing; requires 'OSPF' license

Address          Interface              State           ID               Pri  Dead
10.0.0.26        et-0/0/0.0             Full            33.33.33.11        1    33
10.0.0.30        et-0/0/1.0             Full            33.33.33.22        1    37
10.0.0.22        et-0/0/2.0             Full            22.22.22.22        1    32
10.0.0.13        et-0/0/3.0             Full            11.11.11.22        1    39
10.0.0.5         et-0/0/4.0             Full            11.11.11.11        1    31
```

#### 2. ospf — database — PASS
Command: `show ospf database instance VRF1`
```
 

Warning: License key missing; requires 'OSPF' license


    OSPF database, Area 0.0.0.0
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len 
Router   9.9.9.9          9.9.9.9          0x80000016  1841  0x22 0xa982  48
Router   11.11.11.11      11.11.11.11      0x8000001d   578  0x22 0xae77  60
Router   11.11.11.22      11.11.11.22      0x80000019   795  0x2  0x18ec  60
Router  *22.22.22.11      22.22.22.11      0x80000013   788  0x22 0x2df4  84
Router   22.22.22.22      22.22.22.22      0x8000001b  1483  0x22 0xd16   96
Router   33.33.33.11      33.33.33.11      0x8000001b   586  0x22 0x2466  48
Router   33.33.33.22      33.33.33.22      0x8000001a   842  0x22 0x4b1a  48
Network  10.0.0.1         11.11.11.11      0x80000013   825  0x22 0xcbc4  32
Network  10.0.0.5         11.11.11.11      0x80000013   578  0x22 0x96df  32
Network  10.0.0.9         11.11.11.11      0x80000013   825  0x22 0x95e   32
Network  10.0.0.13        11.11.11.22      0x80000015   795  0x2  0xf77e  32
Network  10.0.0.18        22.22.22.22      0x80000015    43  0x22 0x49db  32
Network  10.0.0.22        22.22.22.22      0x80000014  1483  0x22 0x16f5  32
Network  10.0.0.26        33.33.33.11      0x80000013   586  0x22 0xc319  32
Network  10.0.0.30        33.33.33.22      0x80000013   842  0x22 0xc7fa  32
Network  10.0.0.33        22.22.22.22      0x80000014  1723  0x22 0x35aa  32
Network  10.0.0.37        22.22.22.22      0x80000014  1723  0x22 0xa729  32
Network  10.0.0.42        22.22.22.22      0x80000015    43  0x22 0x59c6  32
Summary  10.1.1.0         11.11.11.11      0x80000013   825  0x22 0xe404  28
Summary  10.1.1.0         11.11.11.22      0x80000018  1105  0x2  0x662e  28
Summary  192.168.41.1     11.11.11.11      0x80000013   825  0x22 0x858   28
Summary  192.168.41.1     11.11.11.22      0x80000015  1135  0x2  0x2bed  28
Summary  192.168.42.1     11.11.11.11      0x80000013   825  0x22 0x57fe  28
Summary  192.168.42.1     11.11.11.22      0x80000016  1105  0x2  0x7895  28
Summary  192.168.43.1     11.11.11.11      0x80000013   825  0x22 0x4c09  28
Summary  192.168.43.1     11.11.11.22      0x80000016  1110  0x2  0x6d9f  28
Summary  192.168.44.1     11.11.11.11      0x80000013   825  0x22 0xe676  28
Summary  192.168.44.1     11.11.11.22      0x80000016  1130  0x2  0x80d   28
    OSPF AS SCOPE link state database
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len 
Extern   0.0.0.0          33.33.33.11      0x80000013   847  0x20 0x367c  36
Extern   0.0.0.0          33.33.33.22      0x80000013   842  0x20 0xf3b3  36
Extern   10.10.10.0       11.11.11.11      0x80000013   825  0x20 0x794e  36
Extern   10.10.10.4       11.11.11.11      0x80000013   825  0x20 0x5172  36
Extern   10.10.10.8       11.11.11.11      0x80000013   825  0x20 0x2996  36
Extern   172.16.110.1     11.11.11.11      0x80000013   825  0x20 0xa610  36
Extern   172.16.210.1     11.11.11.11      0x80000013   825  0x20 0x56fb  36
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

#### 7. interfaces — interface_status — PASS
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

### D2B — aruba_aoscx (aos)

#### 1. ospf — neighbors — PASS
Command: `show ip ospf neighbors vrf default`
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
Command: `show ip ospf lsdb vrf default`
```
OSPF Router with ID (11.11.11.22) (Process ID 1 VRF default)
=============================================================

Router Link State Advertisements (Area 0.0.0.0)
------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum       Link Count
-------------------------------------------------------------------------------
9.9.9.9         9.9.9.9         1844      0x80000016 0x0000a982     2
11.11.11.11     11.11.11.11     582       0x8000001d 0x0000ae77     3
11.11.11.22     11.11.11.22     796       0x80000019 0x000018ec     3
22.22.22.11     22.22.22.11     794       0x80000013 0x00002df4     5
22.22.22.22     22.22.22.22     1486      0x8000001b 0x00000d16     6
33.33.33.11     33.33.33.11     590       0x8000001b 0x00002466     2
33.33.33.22     33.33.33.22     846       0x8000001a 0x00004b1a     2

Network Link State Advertisements (Area 0.0.0.0)
-------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
10.0.0.1        11.11.11.11     827       0x80000013 0x0000cbc4
10.0.0.5        11.11.11.11     583       0x80000013 0x000096df
10.0.0.9        11.11.11.11     828       0x80000013 0x0000095e
10.0.0.13       11.11.11.22     797       0x80000015 0x0000f77e
10.0.0.18       22.22.22.22     47        0x80000015 0x000049db
10.0.0.22       22.22.22.22     1487      0x80000014 0x000016f5
10.0.0.26       33.33.33.11     591       0x80000013 0x0000c319
10.0.0.30       33.33.33.22     847       0x80000013 0x0000c7fa
10.0.0.33       22.22.22.22     1727      0x80000014 0x000035aa
10.0.0.37       22.22.22.22     1727      0x80000014 0x0000a729
10.0.0.42       22.22.22.22     47        0x80000015 0x000059c6

Inter-area Summary Link State Advertisements (Area 0.0.0.0)
------------------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
10.1.1.0        11.11.11.11     828       0x80000013 0x0000e404
10.1.1.0        11.11.11.22     1107      0x80000018 0x0000662e
192.168.41.1    11.11.11.11     828       0x80000013 0x00000858
192.168.41.1    11.11.11.22     1137      0x80000015 0x00002bed
192.168.42.1    11.11.11.11     828       0x80000013 0x000057fe
192.168.42.1    11.11.11.22     1107      0x80000016 0x00007895
192.168.43.1    11.11.11.11     828       0x80000013 0x00004c09
192.168.43.1    11.11.11.22     1111      0x80000016 0x00006d9f
192.168.44.1    11.11.11.11     828       0x80000013 0x0000e676
192.168.44.1    11.11.11.22     1132      0x80000016 0x0000080d

Router Link State Advertisements (Area 0.0.0.1)
------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum       Link Count
-------------------------------------------------------------------------------
1.1.1.1         1.1.1.1         957       0x80000019 0x00006ed4     3
2.2.2.2         2.2.2.2         1787      0x80000017 0x0000da06     3
3.3.3.3         3.3.3.3         1786      0x80000017 0x0000af08     3
4.4.4.4         4.4.4.4         1212      0x80000019 0x0000b314     3
11.11.11.11     11.11.11.11     829       0x8000001e 0x00001089     4
11.11.11.22     11.11.11.22     1102      0x8000001b 0x0000f42c     4

Network Link State Advertisements (Area 0.0.0.1)
-------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
10.1.1.2        11.11.11.11     829       0x80000013 0x0000388a
10.1.1.5        1.1.1.1         1180      0x80000015 0x0000609a
10.1.1.10       11.11.11.11     829       0x80000013 0x00001a9c
10.1.1.13       2.2.2.2         1787      0x80000014 0x00003497
10.1.1.18       11.11.11.11     829       0x80000013 0x0000fbae
10.1.1.21       3.3.3.3         1786      0x80000014 0x0000e7d3
10.1.1.26       11.11.11.11     829       0x80000013 0x0000ddc0
10.1.1.29       4.4.4.4         916       0x80000015 0x00007b4f

Inter-area Summary Link State Advertisements (Area 0.0.0.1)
------------------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
0.0.0.0         11.11.11.11     829       0x80000013 0x000042bd
0.0.0.0         11.11.11.22     1147      0x80000015 0x0000dd35
10.0.0.0        11.11.11.11     829       0x80000013 0x000008e7
10.0.0.0        11.11.11.22     1151      0x80000015 0x00002b7d
10.0.0.4        11.11.11.11     829       0x80000013 0x0000df0c
10.0.0.4        11.11.11.22     790       0x80000016 0x00000b97
10.0.0.8        11.11.11.11     829       0x80000013 0x0000b730
10.0.0.8        11.11.11.22     1142      0x80000015 0x00003f57
10.0.0.12       11.11.11.11     583       0x80000015 0x0000954b
10.0.0.12       11.11.11.22     1151      0x80000015 0x0000b2e9
10.0.0.16       11.11.11.11     829       0x80000013 0x0000cb0a
10.0.0.16       11.11.11.22     1152      0x80000015 0x00008a0e
10.0.0.20       11.11.11.11     583       0x80000014 0x00004792
10.0.0.20       11.11.11.22     790       0x80000017 0x00006829
10.0.0.24       11.11.11.11     583       0x80000014 0x00001fb6
10.0.0.24       11.11.11.22     790       0x80000016 0x0000424c
10.0.0.28       11.11.11.11     583       0x80000014 0x0000f6da
10.0.0.28       11.11.11.22     790       0x80000016 0x00001a70
10.0.0.32       11.11.11.11     583       0x80000014 0x0000d8f3
10.0.0.32       11.11.11.22     790       0x80000017 0x0000f98a
... (19 more lines truncated)
```

#### 3. ospf — borders — PASS
Command: `show ip ospf border-routers vrf default`
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
Command: `show ip ospf vrf default`
```
VRF : default                          Process  : 1
----------------------------------------------------

RouterID           : 11.11.11.22         OSPFv2                 : Enabled         
BFD                : Disabled            SPF Start Interval     : 200   ms
SPF Hold Interval  : 1000  ms            SPF Max Wait Interval  : 5000  ms
LSA Start Time     : 5000  ms            LSA Hold Time          : 0     ms
LSA Max Wait Time  : 0     ms            LSA Arrival            : 1000  ms
External LSAs      : 7                   Checksum Sum           : 203664              
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
Number of LSAs         : 28             Checksum Sum         : 759967
Area  : 0.0.0.1
----------------
Area Type              : Stub           Status               : Active         
Total Interfaces       : 4              Active Interfaces    : 4              
Passive Interfaces     : 0              Loopback Interfaces  : 0
SPF Calculation Count  : 38             
Default Route Cost     : 1    
Area ranges     : 
    ip-prefix 10.1.1.0/24, inter-area, advertise
Number of LSAs         : 40             Checksum Sum         : 1387281
```

#### 5. ospf — interfaces — PASS
Command: `show ip ospf interface vrf default`
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
Command: `show ip ospf vrf default`
```
VRF : default                          Process  : 1
----------------------------------------------------

RouterID           : 11.11.11.22         OSPFv2                 : Enabled         
BFD                : Disabled            SPF Start Interval     : 200   ms
SPF Hold Interval  : 1000  ms            SPF Max Wait Interval  : 5000  ms
LSA Start Time     : 5000  ms            LSA Hold Time          : 0     ms
LSA Max Wait Time  : 0     ms            LSA Arrival            : 1000  ms
External LSAs      : 7                   Checksum Sum           : 203664              
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
Number of LSAs         : 28             Checksum Sum         : 759456
Area  : 0.0.0.1
----------------
Area Type              : Stub           Status               : Active         
Total Interfaces       : 4              Active Interfaces    : 4              
Passive Interfaces     : 0              Loopback Interfaces  : 0
SPF Calculation Count  : 38             
Default Route Cost     : 1    
Area ranges     : 
    ip-prefix 10.1.1.0/24, inter-area, advertise
Number of LSAs         : 40             Checksum Sum         : 1387281
```

#### 7. interfaces — interface_status — PASS
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

### A1M — mikrotik_routeros (routeros)

#### 1. ospf — neighbors — PASS
Command: `/routing ospf neighbor print terse without-paging`
```
0 D instance=default area=area1 address=10.1.1.2 priority=1 router-id=11.11.11.11 dr=10.1.1.2 bdr=10.1.1.1 state=Full state-changes=6 adjacency=10h19m46s timeout=32s
1 D instance=default area=area1 address=10.1.1.6 priority=1 router-id=11.11.11.22 dr=10.1.1.5 bdr=10.1.1.6 state=Full state-changes=6 adjacency=10h18m54s timeout=36s




 




[admin@A1M] > 
```

#### 2. ospf — database — PASS
Command: `/routing ospf lsa print without-paging`
```
Flags: S - self-originated, F - flushing, W - wraparound; D - dynamic 
 0 SD instance=default area=area1 type="router" originator=1.1.1.1 id=1.1.1.1 
      sequence=0x80000019 age=948 checksum=0x6ED4 body=
        options=
            type=network id=10.1.1.2 data=10.1.1.1 metric=1
            type=network id=10.1.1.5 data=10.1.1.5 metric=1
            type=stub id=192.168.41.1 data=255.255.255.255 metric=1

 1  D instance=default area=area1 type="router" originator=2.2.2.2 id=2.2.2.2 
      sequence=0x80000017 age=1784 checksum=0xDA06 body=
        options=DC
            type=stub id=192.168.42.1 data=255.255.255.255 metric=10
            type=network id=10.1.1.13 data=10.1.1.13 metric=10
            type=network id=10.1.1.10 data=10.1.1.9 metric=10

 2  D instance=default area=area1 type="router" originator=3.3.3.3 id=3.3.3.3 
      sequence=0x80000017 age=1785 checksum=0xAF08 body=
        options=DC
            type=stub id=192.168.43.1 data=255.255.255.255 metric=10
            type=network id=10.1.1.18 data=10.1.1.17 metric=10
            type=network id=10.1.1.21 data=10.1.1.21 metric=10

 3  D instance=default area=area1 type="router" originator=4.4.4.4 id=4.4.4.4 
      sequence=0x80000019 age=1210 checksum=0xB314 body=
        options=
            type=network id=10.1.1.26 data=10.1.1.25 metric=1
            type=network id=10.1.1.29 data=10.1.1.29 metric=1
            type=stub id=192.168.44.1 data=255.255.255.255 metric=1

 4  D instance=default area=area1 type="router" originator=11.11.11.11 
      id=11.11.11.11 sequence=0x8000001E age=827 checksum=0x1089 
      body=
        options=DC bits=B
            type=network id=10.1.1.26 data=10.1.1.26 metric=10
            type=network id=10.1.1.18 data=10.1.1.18 metric=10
            type=network id=10.1.1.10 data=10.1.1.10 metric=10
            type=network id=10.1.1.2 data=10.1.1.2 metric=10

 5  D instance=default area=area1 type="router" originator=11.11.11.22 
      id=11.11.11.22 sequence=0x8000001B age=1104 checksum=0xF42C 
      body=
        options= bits=B
            type=network id=10.1.1.5 data=10.1.1.6 metric=100
            type=network id=10.1.1.13 data=10.1.1.14 metric=100
            type=network id=10.1.1.21 data=10.1.1.22 metric=100
            type=network id=10.1.1.29 data=10.1.1.30 metric=100

 6  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.2 sequence=0x80000013 age=827 checksum=0x388A 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=1.1.1.1

 7 SD instance=default area=area1 type="network" originator=1.1.1.1 id=10.1.1.5
      sequence=0x80000015 age=1171 checksum=0x609A 
      body=
        netmask=255.255.255.252
            router-id=1.1.1.1
            router-id=11.11.11.22

 8  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.10 sequence=0x80000013 age=827 checksum=0x1A9C 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=2.2.2.2

 9  D instance=default area=area1 type="network" originator=2.2.2.2 
      id=10.1.1.13 sequence=0x80000014 age=1784 checksum=0x3497 
      body=
        netmask=255.255.255.252
            router-id=2.2.2.2
            router-id=11.11.11.22

10  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.18 sequence=0x80000013 age=827 checksum=0xFBAE 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=3.3.3.3

11  D instance=default area=area1 type="network" originator=3.3.3.3 
      id=10.1.1.21 sequence=0x80000014 age=1785 checksum=0xE7D3 
      body=
        netmask=255.255.255.252
            router-id=3.3.3.3
            router-id=11.11.11.22

12  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.26 sequence=0x80000013 age=827 checksum=0xDDC0 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=4.4.4.4

13  D instance=default area=area1 type="network" originator=4.4.4.4 
      id=10.1.1.29 sequence=0x80000015 age=915 checksum=0x7B4F 
      body=
        netmask=255.255.255.252
... (168 more lines truncated)
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

#### 7. interfaces — interface_status — PASS
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
