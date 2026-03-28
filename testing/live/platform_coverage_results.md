# Platform Coverage Results
*Generated: 2026-03-28 17:14:58 UTC*

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
22.22.22.22       1   FULL/BDR        00:00:37    10.0.0.10       Ethernet1/2
22.22.22.11     128   FULL/BDR        00:00:34    10.0.0.6        Ethernet1/3
11.11.11.22       1   FULL/BDR        00:00:30    10.0.0.2        Ethernet1/1
4.4.4.4         128   FULL/BDR        00:00:38    10.1.1.25       Ethernet1/0
3.3.3.3           1   FULL/BDR        00:00:37    10.1.1.17       Ethernet0/3
2.2.2.2           1   FULL/BDR        00:00:36    10.1.1.9        Ethernet0/2
1.1.1.1         128   FULL/BDR        00:00:38    10.1.1.1        Ethernet0/1
```

#### 2. ospf — database — PASS
Command: `show ip ospf database`
```
            OSPF Router with ID (11.11.11.11) (Process ID 1)

		Router Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum Link count
9.9.9.9         9.9.9.9         461         0x80000019 0x00A385 2         
11.11.11.11     11.11.11.11     748         0x8000001F 0x00AA79 3         
11.11.11.22     11.11.11.22     1395        0x8000001B 0x0014EE 3         
22.22.22.11     22.22.22.11     1990        0x80000014 0x002BF5 5         
22.22.22.22     22.22.22.22     103         0x8000001E 0x000719 6         
33.33.33.11     33.33.33.11     768         0x8000001D 0x002068 2         
33.33.33.22     33.33.33.22     1041        0x8000001C 0x00471C 2         

		Net Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum
10.0.0.1        11.11.11.11     992         0x80000015 0x00C7C6
10.0.0.5        11.11.11.11     748         0x80000015 0x0092E1
10.0.0.9        11.11.11.11     992         0x80000015 0x000560
10.0.0.13       11.11.11.22     1395        0x80000017 0x00F380
10.0.0.18       22.22.22.22     523         0x80000017 0x0045DD
10.0.0.22       22.22.22.22     103         0x80000017 0x0010F8
10.0.0.26       33.33.33.11     768         0x80000015 0x00BF1B
10.0.0.30       33.33.33.22     1041        0x80000015 0x00C3FC
10.0.0.33       22.22.22.22     343         0x80000017 0x002FAD
10.0.0.37       22.22.22.22     343         0x80000017 0x00A12C
10.0.0.42       22.22.22.22     523         0x80000017 0x0055C8

		Summary Net Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum
10.1.1.0        11.11.11.11     992         0x80000015 0x00E006
10.1.1.0        11.11.11.22     1704        0x8000001A 0x006230
192.168.41.1    11.11.11.11     992         0x80000015 0x00045A
192.168.41.1    11.11.11.22     1734        0x80000017 0x0027EF
192.168.42.1    11.11.11.11     992         0x80000015 0x005301
192.168.42.1    11.11.11.22     1704        0x80000018 0x007497
192.168.43.1    11.11.11.11     992         0x80000015 0x00480B
192.168.43.1    11.11.11.22     1708        0x80000018 0x0069A1
192.168.44.1    11.11.11.11     992         0x80000015 0x00E278
192.168.44.1    11.11.11.22     1729        0x80000018 0x00040F

		Router Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum Link count
1.1.1.1         1.1.1.1         1548        0x8000001B 0x006AD6 3         
2.2.2.2         2.2.2.2         401         0x8000001A 0x00D409 3         
3.3.3.3         3.3.3.3         402         0x8000001A 0x00A90B 3         
4.4.4.4         4.4.4.4         22          0x8000001C 0x00AD17 3         
11.11.11.11     11.11.11.11     992         0x80000020 0x000C8B 4         
11.11.11.22     11.11.11.22     1700        0x8000001D 0x00F02E 4         

		Net Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum
10.1.1.2        11.11.11.11     992         0x80000015 0x00348C
10.1.1.5        1.1.1.1         1720        0x80000017 0x005C9C
10.1.1.10       11.11.11.11     992         0x80000015 0x00169E
10.1.1.13       2.2.2.2         401         0x80000017 0x002E9A
10.1.1.18       11.11.11.11     992         0x80000015 0x00F7B0
10.1.1.21       3.3.3.3         402         0x80000017 0x00E1D6
10.1.1.26       11.11.11.11     992         0x80000015 0x00D9C2
10.1.1.29       4.4.4.4         1506        0x80000017 0x007751

		Summary Net Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum
0.0.0.0         11.11.11.11     992         0x80000015 0x003EBF
0.0.0.0         11.11.11.22     1745        0x80000017 0x00D937
10.0.0.0        11.11.11.11     992         0x80000015 0x0004E9
10.0.0.0        11.11.11.22     1749        0x80000017 0x00277F
10.0.0.4        11.11.11.11     992         0x80000015 0x00DB0E
10.0.0.4        11.11.11.22     1389        0x80000018 0x000799
10.0.0.8        11.11.11.11     992         0x80000015 0x00B332
10.0.0.8        11.11.11.22     1740        0x80000017 0x003B59
10.0.0.12       11.11.11.11     748         0x80000017 0x00914D
10.0.0.12       11.11.11.22     1749        0x80000017 0x00AEEB
10.0.0.16       11.11.11.11     992         0x80000015 0x00C70C
10.0.0.16       11.11.11.22     1750        0x80000017 0x008610
10.0.0.20       11.11.11.11     748         0x80000016 0x004394
10.0.0.20       11.11.11.22     1389        0x80000019 0x00642B
10.0.0.24       11.11.11.11     748         0x80000016 0x001BB8
10.0.0.24       11.11.11.22     1389        0x80000018 0x003E4E
10.0.0.28       11.11.11.11     748         0x80000016 0x00F2DC
10.0.0.28       11.11.11.22     1389        0x80000018 0x001672
10.0.0.32       11.11.11.11     748         0x80000016 0x00D4F5
10.0.0.32       11.11.11.22     1389        0x80000019 0x00F58C
10.0.0.36       11.11.11.11     748         0x80000016 0x00AC1A
10.0.0.36       11.11.11.22     1389        0x80000019 0x00CDB0
10.0.0.40       11.11.11.11     992         0x80000015 0x00D6E4
10.0.0.40       11.11.11.22     1730        0x80000018 0x00F77B
10.9.9.1        11.11.11.11     992         0x80000015 0x0005BE
10.9.9.1        11.11.11.22     1730        0x80000017 0x002854

		Type-5 AS External Link States

Link ID         ADV Router      Age         Seq#       Checksum Tag
0.0.0.0         33.33.33.11     1010        0x80000015 0x00327E 1         
0.0.0.0         33.33.33.22     1041        0x80000015 0x00EFB5 1         
10.10.10.0      11.11.11.11     992         0x80000015 0x007550 0         
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
    Hello due in 00:00:03
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
    Hello due in 00:00:05
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
    Hello due in 00:00:05
  Supports Link-local Signaling (LLS)
  Cisco NSF helper support enabled
  IETF NSF helper support enabled
  Can be protected by per-prefix Loop-Free FastReroute
  Can be used for per-prefix Loop-Free FastReroute repair paths
  Not Protected by per-prefix TI-LFA
  Index 1/4/7, flood queue length 0
  Next 0x0(0)/0x0(0)/0x0(0)
  Last flood scan length is 0, maximum is 12
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
 Start time: 00:00:02.388, Time elapsed: 11:31:10.763
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
 Number of external LSA 7. Checksum Sum 0x02FF9E
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
	SPF algorithm last executed 11:23:37.489 ago
	SPF algorithm executed 32 times
	Area ranges are
	Number of LSA 28. Checksum Sum 0x0B1FDC
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
	SPF algorithm last executed 11:28:55.185 ago
	SPF algorithm executed 20 times
	Area ranges are
	   10.1.1.0/24 Active(10) Advertise 
	Number of LSA 40. Checksum Sum 0x148166
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
11.11.11.22     1        VRF1     1   FULL/BDR               00:00:37    10.1.1.14       Ethernet2
11.11.11.11     1        VRF1     1   FULL/DR                00:00:36    10.1.1.10       Ethernet1
```

#### 2. ospf — database — PASS
Command: `show ip ospf database vrf VRF1`
```
            OSPF Router with ID(2.2.2.2) (Instance ID 1) (VRF VRF1)


                 Router Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#         Checksum Link count
3.3.3.3         3.3.3.3         406         0x8000001a   0xa90b   3
4.4.4.4         4.4.4.4         26          0x8000001c   0xad17   3
2.2.2.2         2.2.2.2         403         0x8000001a   0xd409   3
1.1.1.1         1.1.1.1         1552        0x8000001b   0x6ad6   3
11.11.11.11     11.11.11.11     996         0x80000020   0xc8b    4
11.11.11.22     11.11.11.22     1702        0x8000001d   0xf02e   4

                 Network Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#         Checksum
10.1.1.5        1.1.1.1         1724        0x80000017   0x5c9c  
10.1.1.26       11.11.11.11     996         0x80000015   0xd9c2  
10.1.1.2        11.11.11.11     996         0x80000015   0x348c  
10.1.1.18       11.11.11.11     996         0x80000015   0xf7b0  
10.1.1.10       11.11.11.11     996         0x80000015   0x169e  
10.1.1.29       4.4.4.4         1510        0x80000017   0x7751  
10.1.1.21       3.3.3.3         406         0x80000017   0xe1d6  
10.1.1.13       2.2.2.2         403         0x80000017   0x2e9a  

                 Summary Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#         Checksum
10.0.0.4        11.11.11.11     996         0x80000015   0xdb0e  
0.0.0.0         11.11.11.22     1747        0x80000017   0xd937  
0.0.0.0         11.11.11.11     996         0x80000015   0x3ebf  
10.9.9.1        11.11.11.11     996         0x80000015   0x5be   
10.0.0.8        11.11.11.11     996         0x80000015   0xb332  
10.0.0.16       11.11.11.11     996         0x80000015   0xc70c  
10.0.0.32       11.11.11.11     751         0x80000016   0xd4f5  
10.0.0.0        11.11.11.11     996         0x80000015   0x4e9   
10.0.0.0        11.11.11.22     1751        0x80000017   0x277f  
10.0.0.32       11.11.11.22     1393        0x80000019   0xf58c  
10.0.0.16       11.11.11.22     1752        0x80000017   0x8610  
10.0.0.24       11.11.11.11     751         0x80000016   0x1bb8  
10.0.0.40       11.11.11.11     996         0x80000015   0xd6e4  
10.0.0.8        11.11.11.22     1742        0x80000017   0x3b59  
10.0.0.40       11.11.11.22     1732        0x80000018   0xf77b  
10.0.0.24       11.11.11.22     1393        0x80000018   0x3e4e  
10.0.0.12       11.11.11.22     1751        0x80000017   0xaeeb  
10.0.0.20       11.11.11.11     751         0x80000016   0x4394  
10.0.0.36       11.11.11.11     751         0x80000016   0xac1a  
10.0.0.4        11.11.11.22     1393        0x80000018   0x799   
10.0.0.36       11.11.11.22     1393        0x80000019   0xcdb0  
10.0.0.20       11.11.11.22     1393        0x80000019   0x642b  
10.0.0.28       11.11.11.11     751         0x80000016   0xf2dc  
10.0.0.12       11.11.11.11     751         0x80000017   0x914d  
10.0.0.28       11.11.11.22     1393        0x80000018   0x1672  
10.9.9.1        11.11.11.22     1732        0x80000017   0x2854  
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
 Time since last SPF 41020 secs
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
   Number of LSA 40. Checksum Sum 1343846
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
10.0.0.26        et-0/0/0.0             Full            33.33.33.11        1    31
10.0.0.30        et-0/0/1.0             Full            33.33.33.22        1    36
10.0.0.22        et-0/0/2.0             Full            22.22.22.22        1    38
10.0.0.13        et-0/0/3.0             Full            11.11.11.22        1    36
10.0.0.5         et-0/0/4.0             Full            11.11.11.11        1    34
```

#### 2. ospf — database — PASS
Command: `show ospf database instance VRF1`
```
 

Warning: License key missing; requires 'OSPF' license


    OSPF database, Area 0.0.0.0
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len 
Router   9.9.9.9          9.9.9.9          0x80000019   464  0x22 0xa385  48
Router   11.11.11.11      11.11.11.11      0x8000001f   752  0x22 0xaa79  60
Router   11.11.11.22      11.11.11.22      0x8000001b  1399  0x2  0x14ee  60
Router  *22.22.22.11      22.22.22.11      0x80000014  1991  0x22 0x2bf5  84
Router   22.22.22.22      22.22.22.22      0x8000001e   107  0x22 0x719   96
Router   33.33.33.11      33.33.33.11      0x8000001d   770  0x22 0x2068  48
Router   33.33.33.22      33.33.33.22      0x8000001c  1042  0x22 0x471c  48
Network  10.0.0.1         11.11.11.11      0x80000015   996  0x22 0xc7c6  32
Network  10.0.0.5         11.11.11.11      0x80000015   752  0x22 0x92e1  32
Network  10.0.0.9         11.11.11.11      0x80000015   996  0x22 0x560   32
Network  10.0.0.13        11.11.11.22      0x80000017  1399  0x2  0xf380  32
Network  10.0.0.18        22.22.22.22      0x80000017   527  0x22 0x45dd  32
Network  10.0.0.22        22.22.22.22      0x80000017   107  0x22 0x10f8  32
Network  10.0.0.26        33.33.33.11      0x80000015   770  0x22 0xbf1b  32
Network  10.0.0.30        33.33.33.22      0x80000015  1042  0x22 0xc3fc  32
Network  10.0.0.33        22.22.22.22      0x80000017   346  0x22 0x2fad  32
Network  10.0.0.37        22.22.22.22      0x80000017   346  0x22 0xa12c  32
Network  10.0.0.42        22.22.22.22      0x80000017   527  0x22 0x55c8  32
Summary  10.1.1.0         11.11.11.11      0x80000015   996  0x22 0xe006  28
Summary  10.1.1.0         11.11.11.22      0x8000001a  1708  0x2  0x6230  28
Summary  192.168.41.1     11.11.11.11      0x80000015   996  0x22 0x45a   28
Summary  192.168.41.1     11.11.11.22      0x80000017  1737  0x2  0x27ef  28
Summary  192.168.42.1     11.11.11.11      0x80000015   996  0x22 0x5301  28
Summary  192.168.42.1     11.11.11.22      0x80000018  1708  0x2  0x7497  28
Summary  192.168.43.1     11.11.11.11      0x80000015   996  0x22 0x480b  28
Summary  192.168.43.1     11.11.11.22      0x80000018  1712  0x2  0x69a1  28
Summary  192.168.44.1     11.11.11.11      0x80000015   996  0x22 0xe278  28
Summary  192.168.44.1     11.11.11.22      0x80000018  1733  0x2  0x40f   28
    OSPF AS SCOPE link state database
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len 
Extern   0.0.0.0          33.33.33.11      0x80000015  1012  0x20 0x327e  36
Extern   0.0.0.0          33.33.33.22      0x80000015  1042  0x20 0xefb5  36
Extern   10.10.10.0       11.11.11.11      0x80000015   996  0x20 0x7550  36
Extern   10.10.10.4       11.11.11.11      0x80000015   996  0x20 0x4d74  36
Extern   10.10.10.8       11.11.11.11      0x80000015   996  0x20 0x2598  36
Extern   172.16.110.1     11.11.11.11      0x80000015   996  0x20 0xa212  36
Extern   172.16.210.1     11.11.11.11      0x80000015   996  0x20 0x52fd  36
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
9.9.9.9         9.9.9.9         466       0x80000019 0x0000a385     2
11.11.11.11     11.11.11.11     754       0x8000001f 0x0000aa79     3
11.11.11.22     11.11.11.22     1398      0x8000001b 0x000014ee     3
22.22.22.11     22.22.22.11     1995      0x80000014 0x00002bf5     5
22.22.22.22     22.22.22.22     109       0x8000001e 0x00000719     6
33.33.33.11     33.33.33.11     772       0x8000001d 0x00002068     2
33.33.33.22     33.33.33.22     1045      0x8000001c 0x0000471c     2

Network Link State Advertisements (Area 0.0.0.0)
-------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
10.0.0.1        11.11.11.11     999       0x80000015 0x0000c7c6
10.0.0.5        11.11.11.11     754       0x80000015 0x000092e1
10.0.0.9        11.11.11.11     999       0x80000015 0x00000560
10.0.0.13       11.11.11.22     1398      0x80000017 0x0000f380
10.0.0.18       22.22.22.22     528       0x80000017 0x000045dd
10.0.0.22       22.22.22.22     109       0x80000017 0x000010f8
10.0.0.26       33.33.33.11     772       0x80000015 0x0000bf1b
10.0.0.30       33.33.33.22     1045      0x80000015 0x0000c3fc
10.0.0.33       22.22.22.22     348       0x80000017 0x00002fad
10.0.0.37       22.22.22.22     348       0x80000017 0x0000a12c
10.0.0.42       22.22.22.22     528       0x80000017 0x000055c8

Inter-area Summary Link State Advertisements (Area 0.0.0.0)
------------------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
10.1.1.0        11.11.11.11     999       0x80000015 0x0000e006
10.1.1.0        11.11.11.22     1708      0x8000001a 0x00006230
192.168.41.1    11.11.11.11     999       0x80000015 0x0000045a
192.168.41.1    11.11.11.22     1738      0x80000017 0x000027ef
192.168.42.1    11.11.11.11     999       0x80000015 0x00005301
192.168.42.1    11.11.11.22     1708      0x80000018 0x00007497
192.168.43.1    11.11.11.11     999       0x80000015 0x0000480b
192.168.43.1    11.11.11.22     1712      0x80000018 0x000069a1
192.168.44.1    11.11.11.11     999       0x80000015 0x0000e278
192.168.44.1    11.11.11.22     1733      0x80000018 0x0000040f

Router Link State Advertisements (Area 0.0.0.1)
------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum       Link Count
-------------------------------------------------------------------------------
1.1.1.1         1.1.1.1         1553      0x8000001b 0x00006ad6     3
2.2.2.2         2.2.2.2         408       0x8000001a 0x0000d409     3
3.3.3.3         3.3.3.3         407       0x8000001a 0x0000a90b     3
4.4.4.4         4.4.4.4         27        0x8000001c 0x0000ad17     3
11.11.11.11     11.11.11.11     999       0x80000020 0x00000c8b     4
11.11.11.22     11.11.11.22     1703      0x8000001d 0x0000f02e     4

Network Link State Advertisements (Area 0.0.0.1)
-------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
10.1.1.2        11.11.11.11     999       0x80000015 0x0000348c
10.1.1.5        1.1.1.1         1725      0x80000017 0x00005c9c
10.1.1.10       11.11.11.11     999       0x80000015 0x0000169e
10.1.1.13       2.2.2.2         408       0x80000017 0x00002e9a
10.1.1.18       11.11.11.11     999       0x80000015 0x0000f7b0
10.1.1.21       3.3.3.3         407       0x80000017 0x0000e1d6
10.1.1.26       11.11.11.11     999       0x80000015 0x0000d9c2
10.1.1.29       4.4.4.4         1511      0x80000017 0x00007751

Inter-area Summary Link State Advertisements (Area 0.0.0.1)
------------------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
0.0.0.0         11.11.11.11     999       0x80000015 0x00003ebf
0.0.0.0         11.11.11.22     1748      0x80000017 0x0000d937
10.0.0.0        11.11.11.11     999       0x80000015 0x000004e9
10.0.0.0        11.11.11.22     1752      0x80000017 0x0000277f
10.0.0.4        11.11.11.11     999       0x80000015 0x0000db0e
10.0.0.4        11.11.11.22     1391      0x80000018 0x00000799
10.0.0.8        11.11.11.11     999       0x80000015 0x0000b332
10.0.0.8        11.11.11.22     1743      0x80000017 0x00003b59
10.0.0.12       11.11.11.11     754       0x80000017 0x0000914d
10.0.0.12       11.11.11.22     1752      0x80000017 0x0000aeeb
10.0.0.16       11.11.11.11     999       0x80000015 0x0000c70c
10.0.0.16       11.11.11.22     1753      0x80000017 0x00008610
10.0.0.20       11.11.11.11     754       0x80000016 0x00004394
10.0.0.20       11.11.11.22     1391      0x80000019 0x0000642b
10.0.0.24       11.11.11.11     754       0x80000016 0x00001bb8
10.0.0.24       11.11.11.22     1391      0x80000018 0x00003e4e
10.0.0.28       11.11.11.11     754       0x80000016 0x0000f2dc
10.0.0.28       11.11.11.22     1391      0x80000018 0x00001672
10.0.0.32       11.11.11.11     754       0x80000016 0x0000d4f5
10.0.0.32       11.11.11.22     1391      0x80000019 0x0000f58c
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
External LSAs      : 7                   Checksum Sum           : 196510              
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
Number of LSAs         : 28             Checksum Sum         : 729052
Area  : 0.0.0.1
----------------
Area Type              : Stub           Status               : Active         
Total Interfaces       : 4              Active Interfaces    : 4              
Passive Interfaces     : 0              Loopback Interfaces  : 0
SPF Calculation Count  : 38             
Default Route Cost     : 1    
Area ranges     : 
    ip-prefix 10.1.1.0/24, inter-area, advertise
Number of LSAs         : 40             Checksum Sum         : 1343846
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
External LSAs      : 7                   Checksum Sum           : 196510              
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
Number of LSAs         : 28             Checksum Sum         : 729052
Area  : 0.0.0.1
----------------
Area Type              : Stub           Status               : Active         
Total Interfaces       : 4              Active Interfaces    : 4              
Passive Interfaces     : 0              Loopback Interfaces  : 0
SPF Calculation Count  : 38             
Default Route Cost     : 1    
Area ranges     : 
    ip-prefix 10.1.1.0/24, inter-area, advertise
Number of LSAs         : 40             Checksum Sum         : 1343846
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
0 D instance=default area=area1 address=10.1.1.2 priority=1 router-id=11.11.11.11 dr=10.1.1.2 bdr=10.1.1.1 state=Full state-changes=6 adjacency=11h29m50s timeout=30s
1 D instance=default area=area1 address=10.1.1.6 priority=1 router-id=11.11.11.22 dr=10.1.1.5 bdr=10.1.1.6 state=Full state-changes=6 adjacency=11h28m58s timeout=33s




 




[admin@A1M] > 
```

#### 2. ospf — database — PASS
Command: `/routing ospf lsa print without-paging`
```
Flags: S - self-originated, F - flushing, W - wraparound; D - dynamic 
 0 SD instance=default area=area1 type="router" originator=1.1.1.1 id=1.1.1.1 
      sequence=0x8000001B age=1547 checksum=0x6AD6 body=
        options=
            type=network id=10.1.1.2 data=10.1.1.1 metric=1
            type=network id=10.1.1.5 data=10.1.1.5 metric=1
            type=stub id=192.168.41.1 data=255.255.255.255 metric=1

 1  D instance=default area=area1 type="router" originator=2.2.2.2 id=2.2.2.2 
      sequence=0x8000001A age=408 checksum=0xD409 body=
        options=DC
            type=stub id=192.168.42.1 data=255.255.255.255 metric=10
            type=network id=10.1.1.13 data=10.1.1.13 metric=10
            type=network id=10.1.1.10 data=10.1.1.9 metric=10

 2  D instance=default area=area1 type="router" originator=3.3.3.3 id=3.3.3.3 
      sequence=0x8000001A age=409 checksum=0xA90B body=
        options=DC
            type=stub id=192.168.43.1 data=255.255.255.255 metric=10
            type=network id=10.1.1.18 data=10.1.1.17 metric=10
            type=network id=10.1.1.21 data=10.1.1.21 metric=10

 3  D instance=default area=area1 type="router" originator=4.4.4.4 id=4.4.4.4 
      sequence=0x8000001C age=29 checksum=0xAD17 body=
        options=
            type=network id=10.1.1.26 data=10.1.1.25 metric=1
            type=network id=10.1.1.29 data=10.1.1.29 metric=1
            type=stub id=192.168.44.1 data=255.255.255.255 metric=1

 4  D instance=default area=area1 type="router" originator=11.11.11.11 
      id=11.11.11.11 sequence=0x80000020 age=999 checksum=0xC8B 
      body=
        options=DC bits=B
            type=network id=10.1.1.26 data=10.1.1.26 metric=10
            type=network id=10.1.1.18 data=10.1.1.18 metric=10
            type=network id=10.1.1.10 data=10.1.1.10 metric=10
            type=network id=10.1.1.2 data=10.1.1.2 metric=10

 5  D instance=default area=area1 type="router" originator=11.11.11.22 
      id=11.11.11.22 sequence=0x8000001D age=1705 checksum=0xF02E 
      body=
        options= bits=B
            type=network id=10.1.1.5 data=10.1.1.6 metric=100
            type=network id=10.1.1.13 data=10.1.1.14 metric=100
            type=network id=10.1.1.21 data=10.1.1.22 metric=100
            type=network id=10.1.1.29 data=10.1.1.30 metric=100

 6  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.2 sequence=0x80000015 age=999 checksum=0x348C 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=1.1.1.1

 7 SD instance=default area=area1 type="network" originator=1.1.1.1 id=10.1.1.5
      sequence=0x80000017 age=1719 checksum=0x5C9C 
      body=
        netmask=255.255.255.252
            router-id=1.1.1.1
            router-id=11.11.11.22

 8  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.10 sequence=0x80000015 age=999 checksum=0x169E 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=2.2.2.2

 9  D instance=default area=area1 type="network" originator=2.2.2.2 
      id=10.1.1.13 sequence=0x80000017 age=408 checksum=0x2E9A 
      body=
        netmask=255.255.255.252
            router-id=2.2.2.2
            router-id=11.11.11.22

10  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.18 sequence=0x80000015 age=999 checksum=0xF7B0 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=3.3.3.3

11  D instance=default area=area1 type="network" originator=3.3.3.3 
      id=10.1.1.21 sequence=0x80000017 age=409 checksum=0xE1D6 
      body=
        netmask=255.255.255.252
            router-id=3.3.3.3
            router-id=11.11.11.22

12  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.26 sequence=0x80000015 age=999 checksum=0xD9C2 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=4.4.4.4

13  D instance=default area=area1 type="network" originator=4.4.4.4 
      id=10.1.1.29 sequence=0x80000017 age=1513 checksum=0x7751 
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
