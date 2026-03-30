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

## QA Investigation

Run your tests with any framework. When something fails, YANA investigates.

### Test Results

YANA reads JUnit XML results from `results/`. JUnit XML is the de facto standard — produced by pytest (`--junitxml`), pyATS (`--xunit`), Robot Framework (`--xunit`), and most other test runners.

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
  7. Agent investigates:
     - get_status() → confirm backends are active
     - Load protocol skill (skills/ospf/SKILL.md or skills/routing/SKILL.md)
     - query_intent() → expected state
     - get_ospf/get_routing/get_interfaces/traceroute → live state
     - Follow skill decision trees to trace the root cause
     - search_knowledge_base → RFC context
  8. Reports findings (scenario, observed, current state, root cause, RFC basis)
  9. Re-presents remaining failures — user picks next, or stops
```

If multiple failures share a root cause, the agent says so after investigating the first one — the user can skip the rest.

### Interactive Mode

YANA also handles ad-hoc questions outside the QA workflow. The user asks a question directly (e.g. "Why can't E1C reach A2A's loopback?") and the agent follows the same diagnostic process: preflight check via `get_status()`, load the relevant protocol skill, query live devices, search the knowledge base, and synthesize a report with root cause and RFC citation. The full interactive workflow is defined in `CLAUDE.md`.