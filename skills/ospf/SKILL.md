---
name: OSPF Troubleshooting
description: "OSPF adjacency, LSDB, area types, authentication, redistribution, and external routes — symptom-first decision trees with lookup tables"
---

> **PREREQUISITE**: Before using this skill, you MUST have already run `get_interfaces(device)` and `get_ospf(device, "neighbors")` on the target device. If neighbors are missing or fewer than expected, go directly to the **Adjacency Checklist** below — do not read the full skill from the top. If all neighbors are FULL and all interfaces Up/Up, proceed with the relevant symptom section.

# OSPF Troubleshooting Skill

## Scope

OSPF adjacency, LSDB, area types, authentication, redistribution, and external route issues.

**Topology:** Area 0 (backbone): C1J, C2A (core), D1C, D2B (distribution/ABR), E1C, E2C (edge/ASBR), DC1A (data center). Area 1 (stub): A1M, A2A, A3A, A4M (access/leaf). D1C is both ABR and ASBR (redistributes EIGRP into OSPF). E1C and E2C originate the default route into OSPF.

**Defaults:** Hello 10s · Dead 40s (broadcast/P2P) | Hello 30s · Dead 120s (NBMA/P2MP) · AD 110 · Reference BW 100 Mbps

---

## Start Here: Neighbor State

When an OSPF neighbor is not FULL or missing entirely:

```
get_ospf(device, "neighbors")
```

| State | Root Cause |
|-------|-----------|
| FULL | Healthy |
| EXSTART / EXCHANGE | **MTU mismatch** (most common) **or duplicate Router ID**. MTU: `get_interfaces(device)` on both sides — compare MTU. Router ID: if MTU matches, run `get_ospf(device, "details")` on both sides and compare Router IDs — a duplicate RID causes the DD master/slave election to deadlock permanently. |
| LOADING | LSA requests pending — retransmission failing (lossy link, CRC errors) or the requested LSA was prematurely aged out (MaxAge) before delivery. **RFC 2328 defines no Loading-state timeout** — a stuck Loading neighbor persists indefinitely. Check interface errors; if none, advise the operator to reset OSPF on the stuck side. |
| INIT | Hello one-way (my RID not in their Hello): asymmetric link, ingress ACL blocking 224.0.0.5/224.0.0.6, or auth mismatch on one side |
| 2WAY | DR/BDR election only (non-DR/BDR on broadcast) — normal for non-DR routers |
| DOWN | No hellos received: interface down, passive interface, or wrong area |

### Query Reference

| Query | What it returns | Use when |
|-------|----------------|----------|
| `neighbors` | Neighbor state, router-id, interface | Checking adjacency health |
| `interfaces` | Timer values, auth type, passive flag, area, network type, cost | Verifying adjacency parameters (timers, auth, passive, area) |
| `config` | Process-level config (area definitions, redistribution, network statements) | Checking OSPF process config (area types, redistribution, network statements) |
| `database` | LSDB contents (LSA types, ages, router-ids) | Investigating missing routes |
| `borders` | ABR and ASBR identification | Confirming which routers are ABRs/ASBRs |
| `details` | Process-level details (SPF stats, router-id, ABR/ASBR role) | Checking NSSA translation, SPF timers, router role |

### Adjacency Checklist

Verify these items on each side in order. Most use `get_ospf(device, "interfaces")` — items that require a different query note this explicitly. Stop at the first mismatch — fix it first, then re-verify.

1. **Hello/dead timers match on both ends?** Read hello/dead values from `get_ospf(device, "interfaces")` on **each side** and compare them.
   Mismatch → root cause found, stop here.
   **Standard defaults** (broadcast/point-to-point): hello=10, dead=40. NBMA/point-to-multipoint: hello=30, dead=120. Any other dead interval (e.g. 7) is non-standard.
   **Fix direction**: restore the device with non-standard values to defaults — never change correctly-configured devices to match a misconfigured outlier.

2. **Area ID and type match?** Area number must be the same AND area type (normal / stub / NSSA) must agree on both sides. Check with `get_ospf(device, "config")` — look for `area X nssa`, `area X stub`. Mismatched type → adjacency rejected (NSSA sets N-bit in Hello options; normal sets E-bit — mismatch = hellos silently dropped) (RFC 3101 §2.3).

3. **Network type match?** (point-to-point vs broadcast → must match)
   - **Caution:** Network type is NOT exchanged in Hello packets — adjacency can form despite mismatch. But SPF breaks: the P2P side generates Router LSAs without DR info; the broadcast side expects DR-based LSAs. Routes appear in LSDB but next-hops become unreachable. Symptom: neighbors show FULL but routes are missing.

4. **Auth key and type match?** (key-id AND key string, case-sensitive). Verify by checking whether other adjacencies using the same key are healthy. Auth type and key are visible in `get_ospf(device, "interfaces")`.

5. **Interface passive?** (`passive-interface` disables hellos) — check `get_ospf(device, "interfaces")` for passive flag.

6. **MTU match?** (most common cause of EXSTART/EXCHANGE stuck)
   - **Diagnosis:** `get_interfaces(device)` on both sides — compare MTU values. OSPF includes interface MTU in DBD packets (RFC 2328 §10.6); if the received MTU exceeds the local interface MTU, the DBD is rejected and the adjacency stalls in EXSTART/EXCHANGE. The lower-MTU side logs "Nbr X has larger interface MTU".
   - **Fix:** Match MTU on both interfaces. Avoid `ip ospf mtu-ignore` — it masks the symptom and can cause oversized OSPF packets to be dropped in transit.

7. **Router IDs unique?** Run `get_ospf(device, "details")` on both sides and compare Router IDs. A duplicate RID causes DD master/slave election in ExStart to deadlock permanently — the adjacency never leaves ExStart. Fix the misconfigured device; the correct RID is typically the Loopback0 address. Note: this check uses `details`, not `interfaces`.

---

## Symptom: Missing Routes

When a route should be present but is not, check the LSDB first:

```
get_ospf(device, "database")
```

> **Tool scope note:** Use `get_routing(device, "ip_route")` to check the routing table directly. LSDB presence (via `get_ospf(device, "database")`) confirms the route is being flooded — `get_routing` confirms RIB installation. If the LSA is present but the route is missing from `get_routing` output: filtering problem (distribute-list in OSPF config) or forwarding address unreachable (see External Route Issues).

### Diagnosis Path

| LSDB Result | Likely Cause |
|-------------|-------------|
| LSA present | Route may be installed (confirm on-device). If confirmed absent from RIB: filtering problem (distribute-list in OSPF config) or forwarding address unreachable (see External Route Issues). If present with wrong metric: check E1/E2 metric type or cost. |
| LSA absent, area type permits this LSA type | Flooding or origination problem — see rules below for where LSAs should originate. |
| LSA absent, area type blocks this LSA type | Expected — the area type filters this LSA. ABR should inject a default (Type 3) instead. |

**LSA absent and area type should allow it:**
- **Type 5 absent in Area 0** → the ASBR (E1C or E2C for default route; D1C for EIGRP redistribution) is not generating the LSA — check `get_ospf(device, "config")` on the ASBR for the redistribute or `default-information-originate` statement.
- **Type 3 absent for a specific prefix** → the ABR (D1C or D2B) may be suppressing it via `area range not-advertise` — check `get_ospf(device, "config")` on both ABRs.
- **Type 7 absent in Area 1** → see NSSA-Specific Issues section (Area 1 is stub, not NSSA — Type 7 should not appear there; if the question is about an NSSA elsewhere, apply these rules).

---

### LSA Type Lookup

| Type | Name | Who generates | Flooded |
|------|------|---------------|---------|
| 1 | Router LSA | Every router | Within area |
| 2 | Network LSA | DR on broadcast | Within area |
| 3 | Summary LSA | ABR | Between areas |
| 4 | ASBR Summary | ABR | Other areas |
| 5 | External LSA | ASBR | All areas (except stub) |
| 7 | NSSA External | ASBR in NSSA | NSSA only → converted to Type 5 at ABR |

### Area-Type Route Presence Rules

- **Stub**: No Type 5/7. ABR injects inter-area summaries (Type 3) + default. External routes blocked. *(Area 1 in this topology.)*
- **Totally stubby** (stub with `no-summary`): No Type 3/5/7. Only a single default (Type 3) from ABR. Know the difference — look for presence/absence of Type 3 LSAs beyond the default.
- **NSSA**: Type 7 generated by ASBR internally. ABR translates to Type 5 for the backbone. Check both ends: Type 7 in NSSA area, Type 5 in backbone.
- **NSSA Totally Stubby** (`nssa no-summary`): No Type 3/5. Type 7 within area + single default (Type 3) from ABR. Combines NSSA external redistribution with totally stubby inter-area filtering.
- **Backbone Area 0**: All LSA types allowed. *(Area 0 in this topology.)*

---

## Symptom: ABR Route Summarization

ABRs (D1C, D2B in this topology) can summarize inter-area routes using `area X range <network> <mask>`. When active, individual subnets within the range are suppressed and replaced with a single aggregate Type 3 LSA. Adding `not-advertise` suppresses even the aggregate.

**Symptom**: specific subnets from another area are missing, but an aggregate prefix is present.

```
get_ospf(device, "config")    → look for `area X range` on D1C or D2B
get_ospf(device, "database")  → verify the aggregate Type 3 LSA exists
```

To verify whether summarization is part of the network design intent, run:
```
query_intent(device="D1C")
query_intent(device="D2B")
```

This is intentional design, not a fault — verify against design intent before concluding it is a problem.

---

## Symptom: NSSA-Specific Issues

*(Area 1 in this topology is a stub, not NSSA. Apply this section if the topology is extended or if an NSSA area is introduced.)*

When redistributed routes are missing in an NSSA area:

1. **Type 7 LSA not generated** → check `redistribute` config on the ASBR
   ```
   get_ospf(device, "config")
   ```
   Look for the redistribute statement; if missing, that is the issue.

2. **Type 7 present in area but Type 5 missing in backbone** → NSSA ABR translation issue
   - Check ABR has `area X nssa` (not `area X nssa no-redistribution`)
   - Multiple NSSA ABRs? Only the one with highest RID translates; verify with `get_ospf(device, "details")`

3. **Default not propagating into NSSA** → ABR must have `area X nssa default-information-originate`

---

## Symptom: Authentication Failures

When neighbors are stuck in INIT with suspected auth mismatch:

> **Before investigating auth keys**: confirm hello/dead timers match on both sides.
> Timer mismatch and auth key mismatch produce identical symptoms (interface Up/Up, L3 reachable, neighbor count = 0). Timer values and auth type are both visible in `get_ospf(device, "interfaces")`. Check timers first.

```
get_ospf(device, "interfaces")    → shows auth type, timer values, and all OSPF interface details
```

Check: key-id match, key-string match (case-sensitive), MD5 vs plain-text type consistent on both ends.

---

## Symptom: Wrong DR/BDR or No DR Election

DR/BDR election occurs on broadcast/NBMA network types only. Highest priority wins (default 1); ties broken by highest Router ID. Priority 0 = ineligible for DR/BDR.

| Symptom | Cause | Check |
|---------|-------|-------|
| Wrong device is DR | Priority misconfiguration | `get_ospf(device, "interfaces")` — check OSPF priority per interface |
| No DR elected | All priorities set to 0 | Same — at least one device must have priority > 0 |
| DR does not change after reboot of old DR | Non-preemptive election | Expected behavior — current DR keeps role until it fails (RFC 2328 §9.4) |

**Note:** DR election is non-preemptive. A higher-priority router joining the segment later does NOT take over the DR role — it waits until the current DR goes down.

---

## Symptom: External Route Issues

### E1 vs E2 Metric Types (RFC 2328 §16.4)

OSPF supports two external metric types for Type 5 / Type 7 LSAs:

| Type | Cost Calculation | Preference |
|------|-----------------|------------|
| E1 | External metric + internal OSPF cost to ASBR (cumulative) | Always preferred over E2 |
| E2 | External metric only — ignores internal distance | Default on Cisco IOS |

**Critical rule**: E1 **always beats** E2 for the same destination, regardless of numeric values.

In this topology: E1C and E2C both originate the default route as **Type E1** (`default-information-originate always` with `type E1`). D1C redistributes EIGRP as **Type E1** (`metric-type 1`). Verify metric type in `get_ospf(device, "database")`.

**Symptom**: unexpected path taken to an external prefix → check metric type in the database. If E1 and E2 both appear for the same destination, E1 wins unconditionally.

### Forwarding Address in External LSAs (RFC 2328 §12.4.3)

A non-zero forwarding address in a Type 5 or Type 7 LSA instructs routers to send traffic **directly to that IP** rather than through the advertising ASBR.

```
get_ospf(device, "database")    → look for non-zero forwarding address in Type 5/7 LSAs
```

**Symptom**: LSA present in LSDB but route not installed in RIB. If the forwarding address is not reachable via OSPF intra- or inter-area routes, the external route is silently discarded.

> **Tool scope note:** YANA cannot directly verify routing table reachability of the forwarding address. If a non-zero forwarding address is found in the database, advise the operator to run `show ip route <forwarding-address>` on the affected router to confirm reachability.

**Proxy check:** `get_ospf(device, "database")` — look for a Type 1/3 LSA whose prefix covers the forwarding address. If none exists, the forwarding address is very likely unreachable.

---

## Verification Checklist (Post-Fix)

- [ ] All expected neighbors in FULL state — `get_ospf(device, "neighbors")`
- [ ] LSDB shows expected LSA types for the area type — `get_ospf(device, "database")`
- [ ] For redistributed routes: Type 5 present in Area 0 (from E1C/E2C default or D1C EIGRP redistribution)
- [ ] For stub areas: no Type 5 LSAs present in Area 1; default Type 3 from ABR is present
- [ ] RIB installation: advise operator to verify on-device with `show ip route` (outside YANA's tool scope)

---

**References:** RFC 2328 (OSPFv2: neighbor FSM §10, MTU §10.6, external metrics §16.4, forwarding address §12.4.3, DR election §9.4) · RFC 3101 (NSSA: N-bit §2.3, translator election §2.2) · RFC 5709 (OSPF HMAC-SHA auth)
