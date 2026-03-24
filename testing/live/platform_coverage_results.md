# Platform Coverage Results
*Generated: 2026-03-24 12:35:14 UTC*

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
22.22.22.22       1   FULL/BDR        00:00:36    10.0.0.10       Ethernet1/2
22.22.22.11     128   FULL/BDR        00:00:36    10.0.0.6        Ethernet1/3
11.11.11.22       1   FULL/BDR        00:00:34    10.0.0.2        Ethernet1/1
4.4.4.4         128   FULL/BDR        00:00:32    10.1.1.25       Ethernet1/0
3.3.3.3           1   FULL/BDR        00:00:32    10.1.1.17       Ethernet0/3
2.2.2.2           1   FULL/BDR        00:00:33    10.1.1.9        Ethernet0/2
1.1.1.1         128   FULL/BDR        00:00:36    10.1.1.1        Ethernet0/1
```

#### 2. ospf — database — PASS
Command: `show ip ospf database`
```
            OSPF Router with ID (11.11.11.11) (Process ID 1)

		Router Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum Link count
9.9.9.9         9.9.9.9         15          0x8000000B 0x00BF77 2         
11.11.11.11     11.11.11.11     604         0x80000011 0x00C66B 3         
11.11.11.22     11.11.11.22     118         0x8000000E 0x002EE1 3         
22.22.22.11     22.22.22.11     2505        0x8000000A 0x003FEB 5         
22.22.22.22     22.22.22.22     1514        0x8000000F 0x00250A 6         
33.33.33.11     33.33.33.11     452         0x80000010 0x003A5B 2         
33.33.33.22     33.33.33.22     573         0x8000000F 0x00610F 2         

		Net Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum
10.0.0.1        11.11.11.11     868         0x80000008 0x00E1B9
10.0.0.5        11.11.11.11     604         0x80000008 0x00ACD4
10.0.0.9        11.11.11.11     868         0x80000008 0x001F53
10.0.0.13       11.11.11.22     118         0x80000009 0x001072
10.0.0.18       22.22.22.22     1814        0x80000008 0x0063CE
10.0.0.22       22.22.22.22     1514        0x80000008 0x002EE9
10.0.0.26       33.33.33.11     452         0x80000008 0x00D90E
10.0.0.30       33.33.33.22     573         0x80000008 0x00DDEF
10.0.0.33       22.22.22.22     1754        0x80000008 0x004D9E
10.0.0.37       22.22.22.22     1754        0x80000008 0x00BF1D
10.0.0.42       22.22.22.22     14          0x80000009 0x0071BA

		Summary Net Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum
10.1.1.0        11.11.11.11     868         0x80000008 0x00FAF8
10.1.1.0        11.11.11.22     430         0x8000000C 0x007E22
192.168.41.1    11.11.11.11     868         0x80000008 0x001E4D
192.168.41.1    11.11.11.22     458         0x80000009 0x0043E1
192.168.42.1    11.11.11.11     868         0x80000008 0x006DF3
192.168.42.1    11.11.11.22     430         0x8000000A 0x009089
192.168.43.1    11.11.11.11     868         0x80000008 0x0062FD
192.168.43.1    11.11.11.22     430         0x8000000A 0x008593
192.168.44.1    11.11.11.11     868         0x80000008 0x00FC6B
192.168.44.1    11.11.11.22     454         0x8000000A 0x002001

		Router Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum Link count
1.1.1.1         1.1.1.1         468         0x8000000D 0x0086C8 3         
2.2.2.2         2.2.2.2         1813        0x8000000B 0x0009E2 3         
3.3.3.3         3.3.3.3         1815        0x8000000B 0x00E9D8 3         
4.4.4.4         4.4.4.4         546         0x8000000C 0x00CD07 3         
11.11.11.11     11.11.11.11     868         0x80000013 0x00267E 4         
11.11.11.22     11.11.11.22     422         0x8000000F 0x0045E5 4         

		Net Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum
10.1.1.2        11.11.11.11     868         0x80000008 0x004E7F
10.1.1.5        1.1.1.1         706         0x80000009 0x00788E
10.1.1.10       11.11.11.11     868         0x80000008 0x003091
10.1.1.14       11.11.11.22     432         0x80000009 0x00D0F5
10.1.1.18       11.11.11.11     868         0x80000008 0x0012A3
10.1.1.22       11.11.11.22     430         0x80000009 0x00A218
10.1.1.26       11.11.11.11     868         0x80000008 0x00F3B5
10.1.1.29       4.4.4.4         403         0x80000009 0x009343

		Summary Net Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum
0.0.0.0         11.11.11.11     868         0x80000008 0x0058B2
0.0.0.0         11.11.11.22     469         0x80000009 0x00F529
10.0.0.0        11.11.11.11     868         0x80000008 0x001EDC
10.0.0.0        11.11.11.22     469         0x80000009 0x004371
10.0.0.4        11.11.11.11     868         0x80000008 0x00F501
10.0.0.4        11.11.11.22     117         0x8000000A 0x00238B
10.0.0.8        11.11.11.11     868         0x80000008 0x00CD25
10.0.0.8        11.11.11.22     464         0x80000009 0x00574B
10.0.0.12       11.11.11.11     604         0x8000000A 0x00AB40
10.0.0.12       11.11.11.22     470         0x80000009 0x00CADD
10.0.0.16       11.11.11.11     868         0x80000008 0x00E1FE
10.0.0.16       11.11.11.22     469         0x80000009 0x00A202
10.0.0.20       11.11.11.11     604         0x80000009 0x005D87
10.0.0.20       11.11.11.22     117         0x8000000B 0x00801D
10.0.0.24       11.11.11.11     604         0x80000009 0x0035AB
10.0.0.24       11.11.11.22     117         0x8000000A 0x005A40
10.0.0.28       11.11.11.11     604         0x80000009 0x000DCF
10.0.0.28       11.11.11.22     117         0x8000000A 0x003264
10.0.0.32       11.11.11.11     604         0x80000009 0x00EEE8
10.0.0.32       11.11.11.22     102         0x8000000B 0x00127E
10.0.0.36       11.11.11.11     604         0x80000009 0x00C60D
10.0.0.36       11.11.11.22     117         0x8000000B 0x00E9A2
10.0.0.40       11.11.11.11     868         0x80000008 0x00F0D7
10.0.0.40       11.11.11.22     425         0x8000000A 0x00146D
10.9.9.1        11.11.11.11     868         0x80000008 0x001FB1
10.9.9.1        11.11.11.22     425         0x8000000A 0x004247

		Type-5 AS External Link States

Link ID         ADV Router      Age         Seq#       Checksum Tag
0.0.0.0         33.33.33.11     940         0x80000008 0x004C71 1         
0.0.0.0         33.33.33.22     573         0x80000008 0x000AA8 1         
10.10.10.0      11.11.11.11     868         0x80000008 0x008F43 0         
... (4 more lines truncated)
```

#### 3. ospf — borders — PASS
Command: `show ip ospf border-routers`
```
            OSPF Router with ID (11.11.11.11) (Process ID 1)


		Base Topology (MTID 0)

Internal Router Routing Table
Codes: i - Intra-area route, I - Inter-area route

i 9.9.9.9 [20] via 10.0.0.10, Ethernet1/2, ASBR, Area 0, SPF 30
i 33.33.33.11 [11] via 10.0.0.6, Ethernet1/3, ASBR, Area 0, SPF 30
i 33.33.33.22 [11] via 10.0.0.6, Ethernet1/3, ASBR, Area 0, SPF 30
i 22.22.22.22 [10] via 10.0.0.10, Ethernet1/2, ASBR, Area 0, SPF 30
i 11.11.11.22 [11] via 10.1.1.25, Ethernet1/0, ABR, Area 1, SPF 20
i 11.11.11.22 [10] via 10.0.0.2, Ethernet1/1, ABR, Area 0, SPF 30
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
    Hello due in 00:00:06
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
    Hello due in 00:00:01
  Supports Link-local Signaling (LLS)
  Cisco NSF helper support enabled
  IETF NSF helper support enabled
  Can be protected by per-prefix Loop-Free FastReroute
  Can be used for per-prefix Loop-Free FastReroute repair paths
  Not Protected by per-prefix TI-LFA
  Index 1/2/2, flood queue length 0
  Next 0x0(0)/0x0(0)/0x0(0)
  Last flood scan length is 1, maximum is 12
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
    Hello due in 00:00:09
  Supports Link-local Signaling (LLS)
  Cisco NSF helper support enabled
  IETF NSF helper support enabled
  Can be protected by per-prefix Loop-Free FastReroute
  Can be used for per-prefix Loop-Free FastReroute repair paths
  Not Protected by per-prefix TI-LFA
  Index 1/1/1, flood queue length 0
  Next 0x0(0)/0x0(0)/0x0(0)
  Last flood scan length is 1, maximum is 12
  Last flood scan time is 0 msec, maximum is 0 msec
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
  Last flood scan length is 1, maximum is 12
  Last flood scan time is 0 msec, maximum is 0 msec
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
 Start time: 00:00:01.774, Time elapsed: 04:10:17.218
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
 Number of external LSA 7. Checksum Sum 0x02B643
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
	SPF algorithm last executed 04:02:12.791 ago
	SPF algorithm executed 30 times
	Area ranges are
	Number of LSA 28. Checksum Sum 0x0D1A5D
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
	SPF algorithm last executed 04:07:35.879 ago
	SPF algorithm executed 20 times
	Area ranges are
	   10.1.1.0/24 Active(10) Advertise 
	Number of LSA 40. Checksum Sum 0x136586
	Number of opaque link LSA 0. Checksum Sum 0x000000
	Number of DCbitless LSA 20
	Number of indication LSA 0
	Number of DoNotAge LSA 0
	Flood list length 0
 Maintenance Mode ID:     131975011281616
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
11.11.11.22     1        VRF1     1   FULL/DR                00:00:37    10.1.1.14       Ethernet2
11.11.11.11     1        VRF1     1   FULL/DR                00:00:32    10.1.1.10       Ethernet1
```

#### 2. ospf — database — PASS
Command: `show ip ospf database vrf VRF1`
```
            OSPF Router with ID(2.2.2.2) (Instance ID 1) (VRF VRF1)


                 Router Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#         Checksum Link count
3.3.3.3         3.3.3.3         1819        0x8000000b   0xe9d8   3
4.4.4.4         4.4.4.4         551         0x8000000c   0xcd07   3
2.2.2.2         2.2.2.2         1815        0x8000000b   0x9e2    3
1.1.1.1         1.1.1.1         472         0x8000000d   0x86c8   3
11.11.11.11     11.11.11.11     872         0x80000013   0x267e   4
11.11.11.22     11.11.11.22     424         0x8000000f   0x45e5   4

                 Network Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#         Checksum
10.1.1.5        1.1.1.1         710         0x80000009   0x788e  
10.1.1.14       11.11.11.22     436         0x80000009   0xd0f5  
10.1.1.26       11.11.11.11     872         0x80000008   0xf3b5  
10.1.1.2        11.11.11.11     872         0x80000008   0x4e7f  
10.1.1.18       11.11.11.11     872         0x80000008   0x12a3  
10.1.1.10       11.11.11.11     872         0x80000008   0x3091  
10.1.1.22       11.11.11.22     432         0x80000009   0xa218  
10.1.1.29       4.4.4.4         408         0x80000009   0x9343  

                 Summary Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#         Checksum
10.0.0.4        11.11.11.11     872         0x80000008   0xf501  
0.0.0.0         11.11.11.22     471         0x80000009   0xf529  
0.0.0.0         11.11.11.11     872         0x80000008   0x58b2  
10.9.9.1        11.11.11.11     872         0x80000008   0x1fb1  
10.0.0.8        11.11.11.11     872         0x80000008   0xcd25  
10.0.0.16       11.11.11.11     872         0x80000008   0xe1fe  
10.0.0.32       11.11.11.11     608         0x80000009   0xeee8  
10.0.0.0        11.11.11.11     872         0x80000008   0x1edc  
10.0.0.0        11.11.11.22     471         0x80000009   0x4371  
10.0.0.32       11.11.11.22     104         0x8000000b   0x127e  
10.0.0.16       11.11.11.22     471         0x80000009   0xa202  
10.0.0.24       11.11.11.11     608         0x80000009   0x35ab  
10.0.0.40       11.11.11.11     872         0x80000008   0xf0d7  
10.0.0.8        11.11.11.22     466         0x80000009   0x574b  
10.0.0.40       11.11.11.22     427         0x8000000a   0x146d  
10.0.0.24       11.11.11.22     119         0x8000000a   0x5a40  
10.0.0.12       11.11.11.22     472         0x80000009   0xcadd  
10.0.0.20       11.11.11.11     608         0x80000009   0x5d87  
10.0.0.36       11.11.11.11     608         0x80000009   0xc60d  
10.0.0.4        11.11.11.22     119         0x8000000a   0x238b  
10.0.0.36       11.11.11.22     119         0x8000000b   0xe9a2  
10.0.0.20       11.11.11.22     119         0x8000000b   0x801d  
10.0.0.28       11.11.11.11     608         0x80000009   0xdcf   
10.0.0.12       11.11.11.11     608         0x8000000a   0xab40  
10.0.0.28       11.11.11.22     119         0x8000000a   0x3264  
10.9.9.1        11.11.11.22     427         0x8000000a   0x4247  
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
  Transmit Delay is 1 sec, State Backup DR, Priority 1
  Interface Speed: 1000 mbps
  Designated Router is 11.11.11.22
  Backup Designated Router is 2.2.2.2
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
 Time since last SPF 14530 secs
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
   SPF algorithm executed 20 times
   Number of LSA 40. Checksum Sum 1271174
   Number of opaque link LSA 0. Checksum Sum 0
   Number of opaque area LSA 0. Checksum Sum 0
   Number of indication LSA 0
   Number of DC-clear LSA 20
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
10.0.0.26        et-0/0/0.0             Full            33.33.33.11        1    39
10.0.0.30        et-0/0/1.0             Full            33.33.33.22        1    37
10.0.0.22        et-0/0/2.0             Full            22.22.22.22        1    36
10.0.0.13        et-0/0/3.0             Full            11.11.11.22        1    38
10.0.0.5         et-0/0/4.0             Full            11.11.11.11        1    32
```

#### 2. ospf — database — PASS
Command: `show ospf database instance VRF1`
```
 

Warning: License key missing; requires 'OSPF' license


    OSPF database, Area 0.0.0.0
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len 
Router   9.9.9.9          9.9.9.9          0x8000000b    18  0x22 0xbf77  48
Router   11.11.11.11      11.11.11.11      0x80000011   609  0x22 0xc66b  60
Router   11.11.11.22      11.11.11.22      0x8000000e   122  0x2  0x2ee1  60
Router  *22.22.22.11      22.22.22.11      0x8000000a  2506  0x22 0x3feb  84
Router   22.22.22.22      22.22.22.22      0x8000000f  1517  0x22 0x250a  96
Router   33.33.33.11      33.33.33.11      0x80000010   454  0x22 0x3a5b  48
Router   33.33.33.22      33.33.33.22      0x8000000f   576  0x22 0x610f  48
Network  10.0.0.1         11.11.11.11      0x80000008   872  0x22 0xe1b9  32
Network  10.0.0.5         11.11.11.11      0x80000008   609  0x22 0xacd4  32
Network  10.0.0.9         11.11.11.11      0x80000008   872  0x22 0x1f53  32
Network  10.0.0.13        11.11.11.22      0x80000009   122  0x2  0x1072  32
Network  10.0.0.18        22.22.22.22      0x80000008  1817  0x22 0x63ce  32
Network  10.0.0.22        22.22.22.22      0x80000008  1517  0x22 0x2ee9  32
Network  10.0.0.26        33.33.33.11      0x80000008   454  0x22 0xd90e  32
Network  10.0.0.30        33.33.33.22      0x80000008   576  0x22 0xddef  32
Network  10.0.0.33        22.22.22.22      0x80000008  1757  0x22 0x4d9e  32
Network  10.0.0.37        22.22.22.22      0x80000008  1757  0x22 0xbf1d  32
Network  10.0.0.42        22.22.22.22      0x80000009    17  0x22 0x71ba  32
Summary  10.1.1.0         11.11.11.11      0x80000008   872  0x22 0xfaf8  28
Summary  10.1.1.0         11.11.11.22      0x8000000c   433  0x2  0x7e22  28
Summary  192.168.41.1     11.11.11.11      0x80000008   872  0x22 0x1e4d  28
Summary  192.168.41.1     11.11.11.22      0x80000009   462  0x2  0x43e1  28
Summary  192.168.42.1     11.11.11.11      0x80000008   872  0x22 0x6df3  28
Summary  192.168.42.1     11.11.11.22      0x8000000a   434  0x2  0x9089  28
Summary  192.168.43.1     11.11.11.11      0x80000008   872  0x22 0x62fd  28
Summary  192.168.43.1     11.11.11.22      0x8000000a   433  0x2  0x8593  28
Summary  192.168.44.1     11.11.11.11      0x80000008   872  0x22 0xfc6b  28
Summary  192.168.44.1     11.11.11.22      0x8000000a   457  0x2  0x2001  28
    OSPF AS SCOPE link state database
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len 
Extern   0.0.0.0          33.33.33.11      0x80000008   942  0x20 0x4c71  36
Extern   0.0.0.0          33.33.33.22      0x80000008   576  0x20 0xaa8   36
Extern   10.10.10.0       11.11.11.11      0x80000008   872  0x20 0x8f43  36
Extern   10.10.10.4       11.11.11.11      0x80000008   872  0x20 0x6767  36
Extern   10.10.10.8       11.11.11.11      0x80000008   872  0x20 0x3f8b  36
Extern   172.16.110.1     11.11.11.11      0x80000008   872  0x20 0xbc05  36
Extern   172.16.210.1     11.11.11.11      0x80000008   872  0x20 0x6cf0  36
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
                                   inet6    fe80::fa7a:faf0:ac:f460-->  
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

2.2.2.2          1         FULL/BDR          10.1.1.13          1/1/3          

3.3.3.3          1         FULL/BDR          10.1.1.21          1/1/4          

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
9.9.9.9         9.9.9.9         21        0x8000000b 0x0000bf77     2
11.11.11.11     11.11.11.11     611       0x80000011 0x0000c66b     3
11.11.11.22     11.11.11.22     122       0x8000000e 0x00002ee1     3
22.22.22.11     22.22.22.11     2510      0x8000000a 0x00003feb     5
22.22.22.22     22.22.22.22     1518      0x8000000f 0x0000250a     6
33.33.33.11     33.33.33.11     457       0x80000010 0x00003a5b     2
33.33.33.22     33.33.33.22     579       0x8000000f 0x0000610f     2

Network Link State Advertisements (Area 0.0.0.0)
-------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
10.0.0.1        11.11.11.11     874       0x80000008 0x0000e1b9
10.0.0.5        11.11.11.11     611       0x80000008 0x0000acd4
10.0.0.9        11.11.11.11     874       0x80000008 0x00001f53
10.0.0.13       11.11.11.22     122       0x80000009 0x00001072
10.0.0.18       22.22.22.22     1819      0x80000008 0x000063ce
10.0.0.22       22.22.22.22     1518      0x80000008 0x00002ee9
10.0.0.26       33.33.33.11     457       0x80000008 0x0000d90e
10.0.0.30       33.33.33.22     579       0x80000008 0x0000ddef
10.0.0.33       22.22.22.22     1758      0x80000008 0x00004d9e
10.0.0.37       22.22.22.22     1758      0x80000008 0x0000bf1d
10.0.0.42       22.22.22.22     19        0x80000009 0x000071ba

Inter-area Summary Link State Advertisements (Area 0.0.0.0)
------------------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
10.1.1.0        11.11.11.11     874       0x80000008 0x0000faf8
10.1.1.0        11.11.11.22     432       0x8000000c 0x00007e22
192.168.41.1    11.11.11.11     874       0x80000008 0x00001e4d
192.168.41.1    11.11.11.22     461       0x80000009 0x000043e1
192.168.42.1    11.11.11.11     874       0x80000008 0x00006df3
192.168.42.1    11.11.11.22     433       0x8000000a 0x00009089
192.168.43.1    11.11.11.11     874       0x80000008 0x000062fd
192.168.43.1    11.11.11.22     432       0x8000000a 0x00008593
192.168.44.1    11.11.11.11     874       0x80000008 0x0000fc6b
192.168.44.1    11.11.11.22     456       0x8000000a 0x00002001

Router Link State Advertisements (Area 0.0.0.1)
------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum       Link Count
-------------------------------------------------------------------------------
1.1.1.1         1.1.1.1         474       0x8000000d 0x000086c8     3
2.2.2.2         2.2.2.2         1819      0x8000000b 0x000009e2     3
3.3.3.3         3.3.3.3         1820      0x8000000b 0x0000e9d8     3
4.4.4.4         4.4.4.4         552       0x8000000c 0x0000cd07     3
11.11.11.11     11.11.11.11     875       0x80000013 0x0000267e     4
11.11.11.22     11.11.11.22     424       0x8000000f 0x000045e5     4

Network Link State Advertisements (Area 0.0.0.1)
-------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
10.1.1.2        11.11.11.11     875       0x80000008 0x00004e7f
10.1.1.5        1.1.1.1         712       0x80000009 0x0000788e
10.1.1.10       11.11.11.11     875       0x80000008 0x00003091
10.1.1.14       11.11.11.22     434       0x80000009 0x0000d0f5
10.1.1.18       11.11.11.11     875       0x80000008 0x000012a3
10.1.1.22       11.11.11.22     432       0x80000009 0x0000a218
10.1.1.26       11.11.11.11     875       0x80000008 0x0000f3b5
10.1.1.29       4.4.4.4         408       0x80000009 0x00009343

Inter-area Summary Link State Advertisements (Area 0.0.0.1)
------------------------------------------------------------

LSID            ADV Router      Age       Seq#       Checksum
--------------------------------------------------------------
0.0.0.0         11.11.11.11     875       0x80000008 0x000058b2
0.0.0.0         11.11.11.22     472       0x80000009 0x0000f529
10.0.0.0        11.11.11.11     875       0x80000008 0x00001edc
10.0.0.0        11.11.11.22     472       0x80000009 0x00004371
10.0.0.4        11.11.11.11     875       0x80000008 0x0000f501
10.0.0.4        11.11.11.22     120       0x8000000a 0x0000238b
10.0.0.8        11.11.11.11     875       0x80000008 0x0000cd25
10.0.0.8        11.11.11.22     466       0x80000009 0x0000574b
10.0.0.12       11.11.11.11     612       0x8000000a 0x0000ab40
10.0.0.12       11.11.11.22     474       0x80000009 0x0000cadd
10.0.0.16       11.11.11.11     876       0x80000008 0x0000e1fe
10.0.0.16       11.11.11.22     473       0x80000009 0x0000a202
10.0.0.20       11.11.11.11     612       0x80000009 0x00005d87
10.0.0.20       11.11.11.22     121       0x8000000b 0x0000801d
10.0.0.24       11.11.11.11     612       0x80000009 0x000035ab
10.0.0.24       11.11.11.22     121       0x8000000a 0x00005a40
10.0.0.28       11.11.11.11     612       0x80000009 0x00000dcf
10.0.0.28       11.11.11.22     121       0x8000000a 0x00003264
10.0.0.32       11.11.11.11     612       0x80000009 0x0000eee8
10.0.0.32       11.11.11.22     106       0x8000000b 0x0000127e
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
 i       11.11.11.11    101   ABR           0.0.0.1      43          10.1.1.5                    1/1/2
 i       11.11.11.11    101   ABR           0.0.0.1      43         10.1.1.29                    1/1/5
 i       11.11.11.11    100  BOTH           0.0.0.0      43          10.0.0.1                    1/1/8
 i           9.9.9.9    110  ASBR           0.0.0.0      43         10.0.0.18                    1/1/6
 i       22.22.22.22    100  ASBR           0.0.0.0      43         10.0.0.18                    1/1/6
 i       33.33.33.11    101  ASBR           0.0.0.0      43         10.0.0.14                    1/1/7
 i       33.33.33.22    101  ASBR           0.0.0.0      43         10.0.0.14                    1/1/7
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
External LSAs      : 7                   Checksum Sum           : 177731              
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
SPF Calculation Count  : 43             
Area ranges     : 
Number of LSAs         : 28             Checksum Sum         : 858717
Area  : 0.0.0.1
----------------
Area Type              : Stub           Status               : Active         
Total Interfaces       : 4              Active Interfaces    : 4              
Passive Interfaces     : 0              Loopback Interfaces  : 0
SPF Calculation Count  : 43             
Default Route Cost     : 1    
Area ranges     : 
    ip-prefix 10.1.1.0/24, inter-area, advertise
Number of LSAs         : 40             Checksum Sum         : 1271174
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
State/Type      : DR                              Router Priority     : 1
DR              : 10.1.1.14                       BDR                 : 10.1.1.13
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
State/Type      : DR                              Router Priority     : 1
DR              : 10.1.1.22                       BDR                 : 10.1.1.21
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
External LSAs      : 7                   Checksum Sum           : 177731              
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
SPF Calculation Count  : 43             
Area ranges     : 
Number of LSAs         : 28             Checksum Sum         : 858717
Area  : 0.0.0.1
----------------
Area Type              : Stub           Status               : Active         
Total Interfaces       : 4              Active Interfaces    : 4              
Passive Interfaces     : 0              Loopback Interfaces  : 0
SPF Calculation Count  : 43             
Default Route Cost     : 1    
Area ranges     : 
    ip-prefix 10.1.1.0/24, inter-area, advertise
Number of LSAs         : 40             Checksum Sum         : 1271174
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
0 D instance=default area=area1 address=10.1.1.2 priority=1 router-id=11.11.11.11 dr=10.1.1.2 bdr=10.1.1.1 state=Full state-changes=6 adjacency=4h8m54s timeout=34s
1 D instance=default area=area1 address=10.1.1.6 priority=1 router-id=11.11.11.22 dr=10.1.1.5 bdr=10.1.1.6 state=Full state-changes=6 adjacency=4h7m41s timeout=35s




 




[admin@A1M] > 
```

#### 2. ospf — database — PASS
Command: `/routing ospf lsa print without-paging`
```
Flags: S - self-originated, F - flushing, W - wraparound; D - dynamic 
 0 SD instance=default area=area1 type="router" originator=1.1.1.1 id=1.1.1.1 
      sequence=0x8000000D age=467 checksum=0x86C8 body=
        options=
            type=network id=10.1.1.2 data=10.1.1.1 metric=1
            type=network id=10.1.1.5 data=10.1.1.5 metric=1
            type=stub id=192.168.41.1 data=255.255.255.255 metric=1

 1  D instance=default area=area1 type="router" originator=2.2.2.2 id=2.2.2.2 
      sequence=0x8000000B age=1820 checksum=0x9E2 body=
        options=DC
            type=stub id=192.168.42.1 data=255.255.255.255 metric=10
            type=network id=10.1.1.14 data=10.1.1.13 metric=10
            type=network id=10.1.1.10 data=10.1.1.9 metric=10

 2  D instance=default area=area1 type="router" originator=3.3.3.3 id=3.3.3.3 
      sequence=0x8000000B age=1821 checksum=0xE9D8 body=
        options=DC
            type=stub id=192.168.43.1 data=255.255.255.255 metric=10
            type=network id=10.1.1.18 data=10.1.1.17 metric=10
            type=network id=10.1.1.22 data=10.1.1.21 metric=10

 3  D instance=default area=area1 type="router" originator=4.4.4.4 id=4.4.4.4 
      sequence=0x8000000C age=553 checksum=0xCD07 body=
        options=
            type=network id=10.1.1.26 data=10.1.1.25 metric=1
            type=network id=10.1.1.29 data=10.1.1.29 metric=1
            type=stub id=192.168.44.1 data=255.255.255.255 metric=1

 4  D instance=default area=area1 type="router" originator=11.11.11.11 
      id=11.11.11.11 sequence=0x80000013 age=875 checksum=0x267E 
      body=
        options=DC bits=B
            type=network id=10.1.1.26 data=10.1.1.26 metric=10
            type=network id=10.1.1.18 data=10.1.1.18 metric=10
            type=network id=10.1.1.10 data=10.1.1.10 metric=10
            type=network id=10.1.1.2 data=10.1.1.2 metric=10

 5  D instance=default area=area1 type="router" originator=11.11.11.22 
      id=11.11.11.22 sequence=0x8000000F age=426 checksum=0x45E5 
      body=
        options= bits=B
            type=network id=10.1.1.5 data=10.1.1.6 metric=100
            type=network id=10.1.1.14 data=10.1.1.14 metric=100
            type=network id=10.1.1.22 data=10.1.1.22 metric=100
            type=network id=10.1.1.29 data=10.1.1.30 metric=100

 6  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.2 sequence=0x80000008 age=875 checksum=0x4E7F 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=1.1.1.1

 7 SD instance=default area=area1 type="network" originator=1.1.1.1 id=10.1.1.5
      sequence=0x80000009 age=705 checksum=0x788E body=
        netmask=255.255.255.252
            router-id=1.1.1.1
            router-id=11.11.11.22

 8  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.10 sequence=0x80000008 age=875 checksum=0x3091 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=2.2.2.2

 9  D instance=default area=area1 type="network" originator=11.11.11.22 
      id=10.1.1.14 sequence=0x80000009 age=436 checksum=0xD0F5 
      body=
        netmask=255.255.255.252
            router-id=2.2.2.2
            router-id=11.11.11.22

10  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.18 sequence=0x80000008 age=875 checksum=0x12A3 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=3.3.3.3

11  D instance=default area=area1 type="network" originator=11.11.11.22 
      id=10.1.1.22 sequence=0x80000009 age=434 checksum=0xA218 
      body=
        netmask=255.255.255.252
            router-id=3.3.3.3
            router-id=11.11.11.22

12  D instance=default area=area1 type="network" originator=11.11.11.11 
      id=10.1.1.26 sequence=0x80000008 age=875 checksum=0xF3B5 
      body=
        netmask=255.255.255.252
            router-id=11.11.11.11
            router-id=4.4.4.4

13  D instance=default area=area1 type="network" originator=4.4.4.4 
      id=10.1.1.29 sequence=0x80000009 age=410 checksum=0x9343 
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

#### 7. interfaces — interface_status — PASS
Command: `/interface print brief without-paging`
```
Flags: R - RUNNING
Columns: NAME, TYPE, ACTUAL-MTU, L2MTU, MAC-ADDRESS
#   NAME    TYPE      ACTUAL-MTU  L2MTU  MAC-ADDRESS      
0 R ether1  ether           1500         0C:00:20:7A:B8:00
;;; TO-D1C
1 R ether2  ether           1500         AA:C1:AB:3C:4D:3A
;;; TO-D2B
2 R ether3  ether           1500         AA:C1:AB:1F:CB:4C
3 R VRF1    vrf            65536         36:54:CC:7F:2B:04
4 R lo      loopback       65536         00:00:00:00:00:00
;;; Loopback0
5 R lo0     bridge          1500  65535  26:98:2D:36:50:6C




 




[admin@A1M] > 
```
