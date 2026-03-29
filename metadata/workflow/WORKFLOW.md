# YANA — How It Works

YANA is an MCP server that gives Claude real-time access to a multi-vendor network. It has two modes of operation: **interactive troubleshooting** (user asks questions, agent investigates) and **automated QA** (Ansible runs health checks, agent investigates failures).

Both modes use the same 8 MCP tools and the same diagnostic workflow — the difference is how the investigation starts.

---

## The Tools

YANA exposes 8 tools registered in `server/MCPServer.py`:

| Tool | Purpose | Backend |
|------|---------|---------|
| `get_status` | Report active data sources (inventory, credentials, intent, KB) | Local checks |
| `list_devices` | List inventory devices, optionally filtered by vendor | `core/inventory.py` |
| `search_knowledge_base` | Semantic search over RFCs and vendor docs | ChromaDB + MiniLM embeddings |
| `query_intent` | Network design intent (roles, OSPF areas, links) | NetBox or `core/legacy/INTENT.json` |
| `get_ospf` | Live OSPF queries (neighbors, database, borders, config, interfaces, details) | SSH via Scrapli |
| `get_interfaces` | Live interface status | SSH via Scrapli |
| `get_routing` | Live routing table and policy data (ip_route, route_maps, prefix_lists, PBR, ACLs) | SSH via Scrapli |
| `traceroute` | Trace forwarding path from a device to a destination | SSH via Scrapli |

### The SSH Pipeline

All live device tools (`get_ospf`, `get_interfaces`, `get_routing`, `traceroute`) share the same execution path:

```
User query
  → Pydantic validation (VRF regex: ^[a-zA-Z0-9_-]{1,32}$)
  → Device lookup (core/inventory.py — loaded from NetBox or NETWORK.json)
  → Command resolution (platforms/platform_map.py — 6 vendors × all query types)
  → SSH execution (transport/ssh.py — Scrapli, semaphore-limited, 1 retry)
  → Response: {device, _command, cli_style, raw}
```

Credentials come from HashiCorp Vault (`yana/router`) with env var fallback. Six vendors are supported: Cisco IOS, Arista EOS, Juniper JunOS, Aruba AOS-CX, MikroTik RouterOS, VyOS.

### The Knowledge Base

`search_knowledge_base` performs RAG (Retrieval-Augmented Generation):

1. **Ingestion** (one-time, via `python ingest.py`): Markdown files from `docs/` are chunked, embedded with `all-MiniLM-L6-v2`, and stored in ChromaDB with metadata (vendor, topic, source).
2. **Query**: The user's question is embedded into the same vector space. ChromaDB returns the top-k most similar chunks by cosine distance.
3. **Filters**: Optional `vendor` and `topic` filters narrow results before similarity search.

Device inventory and design intent are NOT in ChromaDB — they are served live by `list_devices` and `query_intent`.

---

## Mode 1: Interactive Troubleshooting

The user asks a question in Claude Code. The agent follows the diagnostic workflow defined in `CLAUDE.md`:

### Step 0 — Preflight

```
get_status()
```

Confirms which backends are active: inventory source (NetBox or JSON), credential source (Vault or env vars), intent source, and ChromaDB availability. Displayed as a table before any investigation begins.

### Step 1 — Load the Protocol Skill

The agent reads the relevant skill file before starting. Skill files contain decision trees and query sequences — the agent follows them, it does not improvise.

| When to use | Skill file |
|-------------|-----------|
| Adjacency, neighbor state, LSDB, area type | `skills/ospf/SKILL.md` |
| Path selection, PBR, route-maps, prefix-lists, AD conflicts | `skills/routing/SKILL.md` |
| Reachability ("can't reach X from Y") | Start with `traceroute` to find the breaking hop, then load the appropriate skill |

### Step 2 — Search the Knowledge Base

```
search_knowledge_base(query="OSPF neighbor stuck in INIT", topic="rfc")
```

Returns RFC text and vendor documentation relevant to the issue. The embedding model maps the question to nearby chunks even when the exact words differ.

### Step 3 — Query Live Devices

The agent queries the devices involved in the issue:

```
query_intent(device="D1C")        # what SHOULD the network look like?
get_ospf("D1C", "neighbors")      # what DOES it look like?
get_ospf("D1C", "interfaces")     # check timers, area, passive, auth
traceroute("E1C", "192.168.42.1") # where does the path break?
```

The skill file dictates which queries to run and in what order. For OSPF adjacency issues, the checklist is: timers → area type → network type → auth → passive → MTU → interface state. Stop at the first mismatch.

### Step 4 — Synthesize

The agent combines knowledge base context with live data. When they conflict, live data wins. The report states:

- What the data shows
- Root cause with RFC citation
- Fix direction (configuration guidance only — YANA never pushes config)

### Example

```
User: "Why can't E1C reach A2A's loopback?"

Agent:
  1. get_status()           → NetBox, Vault, ChromaDB all active
  2. Reads skills/ospf/SKILL.md
  3. get_routing("E1C", "ip_route")  → 192.168.42.1 missing from VRF1
  4. get_ospf("E1C", "database")     → No Type 3 LSA for 192.168.42.1
  5. query_intent()          → A2A should be in Area 1 (stub), connected via D1C/D2B
  6. get_ospf("D1C", "neighbors")    → D1C has no adjacency with A2A
  7. get_ospf("A2A", "interfaces")   → A2A's Area 1 is "normal", not stub
  8. search_knowledge_base("E-bit mismatch stub area", topic="rfc")

  Report: A2A is missing `area 1 stub`. RFC 2328 §10.5: E-bit mismatch
          causes Hellos to be silently discarded. Fix: add stub config to A2A.
```

---

## Mode 2: Automated QA

Health checks run via Ansible playbooks over NETCONF. When a check fails, the `/qa` skill triggers the same diagnostic workflow.

### How the Tests Run

```
cd ansible && ansible-playbook playbooks/network_qa.yml
```

**Pipeline:**

```
network_qa.yml (entry point)
  → Discovers test cases in ansible/test_cases/*.yml
  → Loops through each, calling _run_check.yml
      → NETCONF GET to the target device (ietf-routing YANG model)
      → Custom Jinja2 filter asserts the expected condition (e.g. route_exists)
      → Records pass/fail with RFC reference and raw output
  → Writes results to ansible/results/results_<timestamp>.json
  → Prints summary: N passed, M failed
```

**Test case format** (example: `test_cases/route_to_a2a.yml`):

```yaml
scenario: route_to_a2a
description: "Verify E1C has route to A2A loopback 192.168.42.1 in VRF1"
rfc_ref: RFC 2328 §16
device: E1C
vrf: VRF1
assert_route_exists: "192.168.42.1"
```

Each test case defines: which device to query, which VRF, and what to assert. The NETCONF connection uses `ietf-routing` YANG for routing table reads. Credentials come from HashiCorp Vault via the `community.hashi_vault` Ansible collection.

### Investigating Failures — `/qa`

When tests fail, the user runs `/qa` in Claude Code. The skill (`/.claude/skills/qa/SKILL.md`) drives a structured investigation:

```
/qa
  1. Load latest results JSON from ansible/results/
  2. Triage: separate passes from failures
  3. Present numbered failure list to the user
  4. User picks a failure to investigate
  5. Agent reads the test case YAML to understand what was checked
  6. Agent runs the same diagnostic workflow as Mode 1:
     - query_intent() → expected state
     - get_ospf/get_routing/get_interfaces → live state
     - Follows skill decision trees to trace the root cause
     - search_knowledge_base → RFC context
  7. Reports findings (scenario, observed, current state, root cause, RFC basis)
  8. Re-presents remaining failures — user picks next, or stops
```

If multiple failures share a root cause, the agent says so after investigating the first one — the user can skip the rest.

### Example

```
User: /qa

Agent:
  Network QA — 0 passed, 1 failed

  Failures:
    1. route_to_a2a   RFC 2328 §16   Verify E1C has route to A2A loopback

  Which failure would you like to investigate?

User: 1

Agent: [runs full investigation — same tools, same skills, same report format as Mode 1]

  Root cause: A2A is missing area 1 stub configuration.
  RFC 2328 §10.5: E-bit mismatch causes Hello packets to be discarded.
  Recovery: network is still broken — A2A remains isolated.
```

---

## Architecture Summary

```
                    ┌─────────────────────────────────────────┐
                    │            Claude Code (UI)              │
                    │                                         │
                    │   Mode 1: User asks a question          │
                    │   Mode 2: User runs /qa after tests     │
                    └──────────────┬──────────────────────────┘
                                   │ MCP protocol
                    ┌──────────────▼──────────────────────────┐
                    │         YANA MCP Server                  │
                    │         server/MCPServer.py              │
                    │                                         │
                    │   8 tools registered via FastMCP         │
                    └──┬───────┬───────┬───────┬──────────────┘
                       │       │       │       │
              ┌────────▼──┐ ┌──▼────┐ ┌▼─────┐ ┌▼──────────┐
              │ SSH tools  │ │ RAG   │ │Intent│ │ Status    │
              │ get_ospf   │ │search │ │query │ │ get_status│
              │ get_routing│ │_kb    │ │_intent││ list_dev  │
              │ get_intf   │ │       │ │      │ │           │
              │ traceroute │ │       │ │      │ │           │
              └─────┬──────┘ └───┬───┘ └──┬───┘ └───────────┘
                    │            │        │
         ┌──────────▼──┐  ┌─────▼───┐ ┌──▼──────┐
         │  Scrapli SSH │  │ChromaDB │ │ NetBox  │
         │  6 vendors   │  │ + MiniLM│ │ or JSON │
         │  Vault creds │  │         │ │         │
         └──────────────┘  └─────────┘ └─────────┘

  Ansible QA (separate process, not MCP):
    ansible-playbook network_qa.yml
      → NETCONF GET via ncclient (ietf-routing YANG)
      → Results JSON → consumed by /qa skill in Claude
```
