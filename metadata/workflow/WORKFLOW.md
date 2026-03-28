# Workflow • From Question to Answer

This document walks through exactly what happens when you ask YANA a question, using real data from the project.

## The Question

```
"Why is D1C's OSPF neighbor stuck in INIT?"
```

## The 8 MCP Tools

YANA exposes eight MCP tools registered in `server/MCPServer.py`. Together they cover the full investigation path from preflight to live device data:

| Tool | Purpose |
|------|---------|
| `get_status` | Report active data sources (inventory, credentials, intent, documentation) |
| `list_devices` | List inventory devices, optionally filtered by CLI style |
| `search_knowledge_base` | RAG search over ChromaDB knowledge base with optional vendor/topic/top\_k filters |
| `get_ospf` | Execute a live OSPF query against any supported device via SSH |
| `get_interfaces` | Execute a live interface status query against any supported device via SSH |
| `get_routing` | Execute a live routing table or policy query against any supported device via SSH |
| `traceroute` | Trace the forwarding path from a device to a destination IP via SSH |
| `query_intent` | Return network design intent for one or all routers |

---

## Step 0: Check Data Sources — `get_status`

At the start of every investigation, the agent calls `get_status` (`tools/status.py`) and displays the result as a table. This confirms which backends are active before any queries run.

`get_status` checks four subsystems:

| Field | Source resolution |
|-------|------------------|
| `inventory` | NetBox DCIM devices (primary) → `core/legacy/NETWORK.json` (fallback) → empty |
| `vault` | HashiCorp Vault path `yana/router` (primary) → env vars `ROUTER_USERNAME` / `ROUTER_PASSWORD` (fallback) |
| `intent` | NetBox config contexts with `yana-` prefix (primary) → `core/legacy/INTENT.json` (fallback) |
| `chromadb` | ChromaDB directory existence check |

Example output when NetBox is available but Vault is not configured:

```
| inventory | netbox       | 16 devices |
| vault     | env          |            |
| intent    | netbox       | 16 routers |
| chromadb  | available    |            |
```

The vault source (`"vault"` vs `"env"`) is tracked by `_sources` in `core/vault.py` — populated as a side-effect of `get_secret()` calls at server startup (`core/settings.py` imports trigger credential resolution).

---

## Step 1: Load the Protocol Skill

Before starting any investigation, the agent reads the relevant skill file. For OSPF that is `skills/ospf/SKILL.md`.

`CLAUDE.md` is the top-level agent instruction file — it defines the troubleshooting workflow itself. Skill files (`skills/<protocol>/SKILL.md`) are protocol-specific documents that contain decision trees, query sequences, and symptom-specific diagnosis paths (e.g. which queries to run when a neighbor is stuck in EXSTART vs. INIT). The agent follows the skill — it does not improvise the diagnostic order.

---

## Step 2: Search the Knowledge Base — `search_knowledge_base`

### 2a. Ingestion (One-Time Setup)

Before any question can be answered, the knowledge base must be built. This happens once when you run `python ingest.py`.

**Loading:** `ingest.py` reads all `.md` files from `docs/`. Each file becomes a LangChain `Document` object with metadata derived from its filename. Device inventory and network intent are **not** stored in ChromaDB — they are served at query time by `query_intent` (from NetBox or a local JSON fallback).

Example — `rfc2328_summary.md` gets metadata:
```json
{"vendor": "all", "topic": "rfc", "source": "rfc2328_summary.md"}
```

**Chunking:** The `RecursiveCharacterTextSplitter` breaks each document into ~800 character chunks (overlap: 100 chars), splitting at section headers and paragraphs to keep chunks coherent.

The full `rfc2328_summary.md` (~4000 chars) becomes multiple chunks. One of them is:

```
- **DOWN**: No Hello packets received from this neighbor. Initial state.
- **INIT**: A Hello was received but the local router's ID was not in the
  neighbor's Hello. One-way communication only.
- **2WAY**: Bidirectional communication confirmed. Both routers see each
  other's Router ID in Hello packets...
- **EXSTART**: Master/slave negotiation for Database Description (DD)
  exchange begins...
```

This chunk is 731 characters. It inherited the metadata `{source: "rfc2328_summary.md", topic: "rfc", vendor: "all"}`.

**Embedding:** The `all-MiniLM-L6-v2` model (running locally, no API call) reads that chunk and produces a vector of 384 numbers:

```
[-0.0302, -0.0195, 0.0166, -0.0345, 0.0212, -0.0464, -0.0415, -0.0128, -0.0797, 0.0049, ... ]
(384 dimensions total)
```

These numbers encode the *meaning* of the text in a mathematical space. Text about similar topics produces similar vectors.

**Storage:** ChromaDB stores the chunk as a record:

```
ID:        1181ff8e-1983-4b59-a772-3374a3b6baa1
Text:      "- **DOWN**: No Hello packets received..."  (731 chars)
Metadata:  {"source": "rfc2328_summary.md", "topic": "rfc", "vendor": "all"}
Vector:    [-0.0302, -0.0195, 0.0166, ...]  (384 floats)
```

This happens for all chunks across all documents. The database is now ready.

### 2b. Query

Now you ask: `"Why is D1C's OSPF neighbor stuck in INIT?"`

**Question → Vector:** The same embedding model converts the question into a 384-dim vector:

```
Question: "Why is D1C's OSPF neighbor stuck in INIT"
Vector:   [0.0193, -0.0532, 0.0135, -0.0071, 0.1528, 0.0054, -0.0898, -0.0029, -0.0993, 0.0045, ...]
```

**Similarity Search:** ChromaDB compares the question vector against all stored chunk vectors using cosine distance. Lower distance = more similar meaning.

Results ranked by relevance:

```
Distance: 0.9453  →  rfc2328_summary.md  — "Common Stuck States and Causes" table
Distance: 1.0184  →  vendor_cisco_ios.md  — Cisco IOS OSPF configuration syntax
Distance: 1.0490  →  vendor_arista_eos.md — Arista EOS VRF configuration
```

The top result (distance 0.9453) is the "Common Stuck States and Causes" chunk — which directly explains INIT, EXSTART, and other stuck states. The system found the right answer even though the question used different words than the stored text.

**Return to Claude:** The top `top_k` chunks (default 5, text + metadata) are returned via the MCP tool response.

### 2c. Search Parameters

`search_knowledge_base` accepts optional filters defined in `input_models/models.py`:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | str (max 500 chars) | required | Free-text search question |
| `vendor` | Literal enum \| None | None | Filter by vendor: `arista_eos`, `cisco_ios`, `juniper_junos`, `aruba_aoscx`, `mikrotik_ros` |
| `topic` | Literal enum \| None | None | Filter by topic: `rfc`, `vendor_guide` |
| `top_k` | int (1–10) | 5 | Number of results to return |

When both `vendor` and `topic` are set, they are combined into a ChromaDB `$and` clause:
```python
{"$and": [{"vendor": "cisco_ios"}, {"topic": "vendor_guide"}]}
```

---

## Step 3: Query Live Data

### `query_intent`

Returns network design intent (`tools/intent.py`). Pass `device="D1C"` for a single router's intent (roles, OSPF areas, direct links, BGP neighbors) or omit to return all routers. Intent is loaded live from NetBox config contexts with the `yana-` prefix (primary) or `core/legacy/INTENT.json` (fallback).

Example response for `device="D1C"`:
```json
{
  "device": "D1C",
  "intent": {
    "roles": ["ABR", "OSPF_AREA0_DISTRIBUTION"],
    "igp": {"ospf": {"router_id": "11.11.11.11", "areas": {"0": [...], "1": [...]}}},
    "direct_links": {"A1M": {"local_interface": "Ethernet0/1", "local_ip": "10.1.1.2"}},
    "bgp": {}
  }
}
```

### Live Device Queries — The SSH Pipeline

`get_ospf`, `get_interfaces`, `get_routing`, and `traceroute` all share the same execution pipeline. Here is the full code path for:
```
get_ospf(device="D1C", query="neighbors", vrf="VRF1")
```

**1. Input validation** (`input_models/models.py`)

Pydantic validates the request before any I/O:
- `query` must be one of the allowed Literal values for the tool (e.g. `"neighbors"` for `get_ospf`)
- `vrf` must match `^[a-zA-Z0-9_-]{1,32}$` or be `None` (injection guard)
- Injection attempts in `vrf` (semicolons, pipes, subshell syntax, Unicode lookalikes, etc.) raise `ValidationError` here

**2. Device lookup** (`core/inventory.py:get_device()`)

Looks up `"D1C"` in the inventory dict loaded from NetBox at startup. Returns:
```python
{"host": "172.20.20.11", "platform": "cisco_iosxe", "cli_style": "ios", "vrf": "VRF1"}
```
Unknown device names raise `KeyError` with the list of known devices, surfaced as a clean error response.

**3. Command resolution** (`platforms/platform_map.py:get_action()`)

Maps the request to a vendor-specific CLI command:

1. `PLATFORM_MAP["ios"]["ospf"]["neighbors"]` → `"show ip ospf neighbor"`
2. IOS handles VRF at the OSPF process level — no VRF keyword in show commands, so the string is returned as-is.

For an EOS device with VRF:
1. `PLATFORM_MAP["eos"]["ospf"]["neighbors"]` → `{"default": "show ip ospf neighbor", "vrf": "show ip ospf neighbor vrf {vrf}"}`
2. `_apply_vrf()` selects the `"vrf"` template and substitutes `{vrf}` with `"VRF1"`:
   ```
   show ip ospf neighbor vrf VRF1
   ```

The platform map supports six vendors, each with three categories:

| Category | Queries |
|----------|---------|
| `ospf` | `neighbors`, `database`, `borders`, `config`, `interfaces`, `details` |
| `interfaces` | `interface_status` |
| `routing_table` | `ip_route`, `route_maps`, `prefix_lists`, `policy_based_routing`, `access_lists` |
| `tools` | `traceroute` |

**4. Transport execution** (`transport/__init__.py` → `transport/ssh.py`)

`execute_command()` acquires a semaphore slot (max 5 concurrent SSH sessions), then calls `execute_ssh()`.

`execute_ssh()` (scrapli2) builds a `Cli` object per device with vendor-specific options:

| cli_style | Notes |
|-----------|-------|
| `ios`, `eos`, `junos`, `aos` | Standard `BinOptions` SSH |
| `routeros` | Username gets `+ct` suffix appended; `\r\n` return char |
| `vyos` | `Ssh2Options` |

Credentials come from `core/settings.py` which reads from Vault (`yana/router`) with env var fallback (`ROUTER_USERNAME`, `ROUTER_PASSWORD`). Per-vendor credentials are supported via Vault paths like `yana/routerios`.

SSH is retried once on failure (2s delay). `OpenException` (host unreachable) is not retried.

The raw CLI output is returned as-is — no normalization layer.

**5. Response envelope** (`transport/__init__.py`)

```python
{
  "device":    "D1C",
  "_command":  "show ip ospf neighbor",
  "cli_style": "ios",
  "raw":       "Neighbor ID  Pri  State  Dead Time  Address    Interface\n1.1.1.1   1  INIT/DR  00:00:38  10.1.1.1  Ethernet0/1\n..."
}
```

---

## Step 4: Synthesize

Combine KB context with live device data. When they conflict, trust the live data — the device is the ground truth.

The agent states clearly:
- What the data shows (e.g. neighbor is in INIT, Hello interval mismatch detected)
- What the root cause is (or what further information is needed)
- Configuration direction only — never suggest or apply device configuration changes

---

## Why This Works

The embedding model maps both *"INIT state means Hello one-way"* and *"Why is D1C's neighbor stuck in INIT"* to nearby points in 384-dimensional space — because they're about the same concept. A keyword search would miss this (the word "stuck" doesn't appear in the RFC text), but vector similarity catches the semantic relationship.

For live data, the flat platform map (`cli_style → category → query → command`) keeps vendor differences explicit and testable. Adding a new vendor means adding one dict entry per category — no inheritance, no runtime dispatch complexity.

---

## Summary

```
Preflight:
  get_status → Inventory / Vault / Intent / ChromaDB sources

Investigation:
  Load skill → skills/ospf/SKILL.md

  Knowledge base:
    Question → Vector (all-MiniLM-L6-v2)
             → Cosine similarity search (ChromaDB)
             → Top-k chunks (text + metadata)

  Intent:
    query_intent → Design intent (NetBox config contexts yana-* | INTENT.json)

  Live device (get_ospf | get_interfaces | get_routing | traceroute):
    Validate input (Pydantic — VRF injection guard)
    → Lookup device (inventory → get_device())
    → Resolve command (platform_map: cli_style → category → query → VRF sub)
    → Execute SSH (scrapli2 — semaphore-limited, 1 retry, per-vendor options)
    → Response envelope {device, _command, cli_style, raw}

  Synthesis:
    KB chunks + Intent + Live data → Grounded answer (trust live data on conflict)
```
