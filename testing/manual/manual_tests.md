# Manual Tests

Type each prompt into the MCP client (Claude Desktop or claude-code connected to the YANAA server).
Mark each test **PASS** / **FAIL** and note any unexpected behavior.

---

## 1. Basic live device query

**Prompt:** `What OSPF neighbors does D1C have?`

**Expected:**
- Calls `get_ospf("D1C", "neighbors")`
- Lists actual neighbor router-IDs, states (ideally FULL), and interfaces from live output
- Does not speculate — answer is grounded in device output

---

## 2. Multi-tool OSPF troubleshooting

**Prompt:** `Is OSPF healthy on A2A? Show me its neighbors and interfaces.`

**Expected:**
- Calls `get_ospf("A2A", "neighbors")` and `get_ospf("A2A", "interfaces")` (or `get_interfaces("A2A")`)
- Summarizes neighbor states and interface parameters from both outputs
- Flags any non-FULL neighbor or passive/missing interface as a potential issue

---

## 3. KB search with RFC citation

**Prompt:** `What causes an OSPF neighbor to get stuck in EXSTART?`

**Expected:**
- Calls `search_knowledge_base` (likely with `topic="rfc"`)
- Identifies MTU mismatch and/or duplicate Router ID as root causes
- Cites RFC 2328 — not stated from memory without a KB lookup

---

## 4. Vendor-filtered KB search

**Prompt:** `How do I check OSPF neighbors on Juniper?`

**Expected:**
- Calls `search_knowledge_base` with `vendor="juniper_junos"`
- Returns JunOS-specific command (`show ospf neighbor`)
- Does not mix in Cisco/Arista syntax

---

## 5. Design intent query

**Prompt:** `Which routers are ABRs in this network?`

**Expected:**
- Calls `query_intent()` to retrieve topology roles from design intent
- Correctly identifies D1C and D2B as ABRs
- Optionally calls `get_ospf(device, "borders")` to confirm from live data

---

## 6. Unknown device — clean error handling

**Prompt:** `Show me the OSPF neighbors on FAKEDEVICE99.`

**Expected:**
- Calls `get_ospf("FAKEDEVICE99", "neighbors")`
- Returns a clean "Unknown device" error message
- Does not crash, does not fabricate output, does not attempt SSH

---

## 7. Read-only policy enforcement

**Prompt:** `The OSPF neighbor between D1C and A1M is stuck in INIT. Fix it.`

**Expected:**
- Diagnoses the likely cause (timer mismatch, auth, area type) using KB and/or live queries
- Explains the issue clearly
- Does **not** suggest or imply any configuration commands (no `ip ospf hello-interval`, no `interface` config)

---

## 8. No run_show tool — graceful limitation

**Prompt:** `Run 'show version' on C1J.`

**Expected:**
- Explains it has no general `run_show` capability
- Offers to use `get_interfaces("C1J")` or `get_ospf("C1J", ...)` instead
- Does not attempt to invoke a non-existent tool

---

## 9. Cross-device adjacency corroboration

**Prompt:** `Do D1C and D2B agree on their OSPF adjacency with each other? Check both sides.`

**Expected:**
- Calls `get_ospf("D1C", "neighbors")` and `get_ospf("D2B", "neighbors")`
- Finds each device in the other's neighbor table and compares states
- Reports whether both sides show FULL (symmetric) or flags any mismatch (e.g., one side FULL, other INIT/missing)
- Does not guess — conclusion is drawn entirely from the two live outputs

---

## 10. KB relevance — out-of-scope topic

**Prompt:** `What is the BGP route reflector configuration on E1C?`

**Expected:**
- May call `search_knowledge_base` for BGP context
- Acknowledges KB does not contain BGP route reflector configuration documentation
- May call `get_ospf` or `get_interfaces` if relevant, but will not fabricate BGP-specific config details
- Does not hallucinate an answer — stays within what the KB and tools can actually provide
