# YANA — How It Works

YANA is framework that gives Claude real-time access to a multi-vendor network. It investigates network QA test failures and ad-hoc issues using live device queries, design intent, and protocol documentation.

---

## The Tools

YANA exposes 8 tools registered in `server/MCPServer.py`:

| Tool | Purpose | Backend |
|------|---------|---------|
| `get_status` | Report active data sources (inventory, intent, KB) | Local checks |
| `list_devices` | List inventory devices, optionally filtered by CLI style | `core/inventory.py` |
| `search_knowledge_base` | Semantic search over RFCs and vendor docs | ChromaDB + MiniLM embeddings |
| `query_intent` | Network design intent (roles, OSPF areas, links) | `data/INTENT.json` |
| `get_ospf` | Live OSPF queries (neighbors, database, borders, config, interfaces, details) | SSH via Scrapli |
| `get_interfaces` | Live interface status | SSH via Scrapli |
| `get_routing` | Live routing table and policy data (ip_route, route_maps, prefix_lists, PBR, ACLs) | SSH via Scrapli |
| `traceroute` | Trace forwarding path from a device to a destination | SSH via Scrapli |

### The SSH Pipeline

All live device tools (`get_ospf`, `get_interfaces`, `get_routing`, `traceroute`) share the same execution path:

```
User query
  → Pydantic validation (VRF regex: ^[a-zA-Z0-9_-]{1,32}$)
  → Device lookup (core/inventory.py — loaded from data/NETWORK.json)
  → Command resolution (platforms/platform_map.py — 6 vendors × all query types)
  → SSH execution (transport/ssh.py — Scrapli, semaphore-limited, 1 retry)
  → Response: {device, _command, cli_style, raw}
```

Credentials come from environment variables (`ROUTER_USERNAME`, `ROUTER_PASSWORD`). Six vendors are supported: Cisco IOS, Arista EOS, Juniper JunOS, Aruba AOS-CX, MikroTik RouterOS, VyOS.

### The Knowledge Base

`search_knowledge_base` performs RAG (Retrieval-Augmented Generation):

1. **Ingestion** (one-time, via `make ingest`): Markdown files from `docs/` are chunked, embedded with `all-MiniLM-L6-v2`, and stored in ChromaDB with metadata (vendor, topic, source, protocol). Each chunk gets a contextual header prepended (`[Source: filename | Protocol: protocol]`) for better embedding quality.
2. **Query**: The user's question is embedded into the same vector space. ChromaDB returns the top-k most similar chunks by cosine distance.
3. **Filters**: Optional `vendor`, `topic`, and `protocol` filters narrow results before similarity search. Compound filtering is supported (e.g., `vendor=cisco_ios` + `protocol=ospf`).

Device inventory and design intent are NOT in ChromaDB — they are served at query time by `list_devices` and `query_intent`.

See [OPTIMIZATIONS.md](../scalability/OPTIMIZATIONS.md) for the full RAG optimization roadmap.

---

## Interactive Investigation

The user asks a question in Claude Code. The agent follows the diagnostic workflow defined in `CLAUDE.md`:

### Step 0 — Preflight

```
get_status()
```

Confirms which backends are active: inventory (device count), intent (router count), and ChromaDB availability. Displayed as a table before any investigation begins.

### Step 1 — Load the Protocol Skill

The agent reads the relevant skill file before starting. Skill files contain decision trees and query sequences — the agent follows them, it does not improvise.

| When to use | Skill file |
|-------------|-----------|
| Adjacency, neighbor state, LSDB, area type | `skills/ospf/SKILL.md` |
| Path selection, PBR, route-maps, prefix-lists, AD conflicts | `skills/routing/SKILL.md` |
| Reachability ("can't reach X from Y") | Start with `traceroute` to find the breaking hop, then load the appropriate skill |

### Step 2 — Search the Knowledge Base

```
search_knowledge_base(query="OSPF neighbor stuck in INIT", topic="rfc", protocol="ospf")
```

Returns RFC text and vendor documentation relevant to the issue. The `protocol` filter eliminates cross-protocol noise. The embedding model maps the question to nearby chunks even when the exact words differ.

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
  1. get_status()           → inventory, intent, ChromaDB all active
  2. Reads skills/ospf/SKILL.md
  3. get_routing("E1C", "ip_route")  → 192.168.42.1 missing from VRF1
  4. get_ospf("E1C", "database")     → No Type 3 LSA for 192.168.42.1
  5. query_intent()          → A2A should be in Area 1 (stub), connected via D1C/D2B
  6. get_ospf("D1C", "neighbors")    → D1C has no adjacency with A2A
  7. get_ospf("A2A", "interfaces")   → A2A's Area 1 is "normal", not stub
  8. search_knowledge_base("E-bit mismatch stub area", topic="rfc", protocol="ospf")

  Report: A2A is missing `area 1 stub`. RFC 2328 §10.5: E-bit mismatch
          causes Hellos to be silently discarded. Fix: add stub config to A2A.
```

---

## QA Investigation

Run your tests with any framework. When something fails, YANA investigates.

### Test Results

YANA reads JUnit XML results from `results/`. JUnit XML is the de facto standard — produced by pytest (`--junitxml`), pyATS (`--xunit`), Robot Framework (`--xunit`), Ansible (junit callback), and most other test runners.

Place your test results in `results/` as `.xml` files. YANA doesn't care how the tests were run — it only needs the results.

### Investigating Failures — `/qa`

When tests fail, the user runs `/qa` in Claude Code. The skill (`.claude/skills/qa/SKILL.md`) drives a structured investigation:

```
/qa
  1. Load the most recently modified .xml file from results/
  2. Parse JUnit XML — each <testcase> is one test, <failure> marks failures
  3. Triage: count passes and failures
  4. Present numbered failure list to the user
  5. User picks a failure to investigate
  6. Agent reads test context from <properties> (device, rfc_ref, description)
  7. Agent runs the same diagnostic workflow as interactive mode:
     - query_intent() → expected state
     - get_ospf/get_routing/get_interfaces → live state
     - Follows skill decision trees to trace the root cause
     - search_knowledge_base → RFC context
  8. Reports findings (scenario, observed, current state, root cause, RFC basis)
  9. Re-presents remaining failures — user picks next, or stops
```

If multiple failures share a root cause, the agent says so after investigating the first one — the user can skip the rest.

### Ansible Demo

A reference Ansible QA implementation is included in `ansible/`. It runs NETCONF health checks and produces JUnit XML results. This is just one example — any test framework that outputs JUnit XML works.

---

## Architecture Summary

```
                    ┌─────────────────────────────────────────┐
                    │            Claude Code (UI)              │
                    │                                         │
                    │   Interactive: User asks a question     │
                    │   QA: User runs /qa after tests         │
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
         ┌──────────▼──┐  ┌─────▼───┐ ┌──▼──────────┐
         │  Scrapli SSH │  │ChromaDB │ │ JSON files  │
         │  6 vendors   │  │ + MiniLM│ │ data/*.json │
         │  env creds   │  │         │ │             │
         └──────────────┘  └─────────┘ └─────────────┘

  Test runners (separate process, not MCP):
    pytest, pyATS, Ansible, Robot Framework, etc.
      → JUnit XML results in results/
      → Consumed by /qa skill in Claude
```
