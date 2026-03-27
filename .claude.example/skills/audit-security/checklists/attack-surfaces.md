# Attack Surfaces — netKB

Use this during Phase 3. This defines every entry point into netKB and the data flow for each user-controlled input.

---

## Trust Boundary Map

```
[MCP Client / Claude LLM]
        |
        | Tool calls (JSON arguments, LLM-generated, untrusted)
        | No authentication layer
        v
[netKB MCP Server — FastMCP]
        |
        |-- search_knowledge_base ──> [ChromaDB / HuggingFace Embeddings] (local)
        |
        |-- get_ospf / get_interfaces
        |       |
        |       |-- Pydantic validation
        |       |-- platforms/platform_map.py (static command resolution)
        |       |-- core/vault.py (credentials)
        |       v
        |   [Scrapli SSH Transport]
        |       |
        |       v
        |   [Network Device] <── UNTRUSTED OUTPUT ──> device CLI output
        |
        v
[NetBox API] (semi-trusted, internal) -- populates inventory
[Vault API]  (trusted, credential store)
[.env file]  (trusted, deployment config)
```

---

## Entry Points

| Entry point | Trust level | Attacker control | Reaches |
|-------------|-------------|-----------------|---------|
| MCP tool arguments | Untrusted (LLM-generated) | All tool parameters | Pydantic validation, then platform_map / inventory |
| NetBox API response | Semi-trusted | Device names, IPs, cli_style values | Error messages, SSH target, credential path |
| Vault API response | Trusted | Secret values (if Vault compromised) | SSH credentials |
| Environment variables | Trusted (deployment) | All settings including credentials | SSH transport, server behavior |
| SSH device output | Untrusted | Raw CLI text | LLM context (via tool response) |
| ChromaDB on-disk files | Trusted (local) | KB document content (if filesystem compromised) | LLM context (via search response) |
| `docs/` markdown | Trusted (developer-written) | KB content ingested into ChromaDB | LLM context after ingest |
| `.github/workflows/ci.yml` | Developer-controlled | CI configuration, secret access | Build and test pipeline |

---

## Data Flow Per User-Controlled Input

### `device` (OspfQuery, InterfacesQuery)
```
MCP tool call
  → Pydantic: no length limit, no character restriction (any string)
  → inventory dict lookup: devices.get(device) → None if unknown
  → if None: error response containing the device name
  → if found: device dict with host, platform, cli_style, vrf
  → host → Scrapli SSH target
  → cli_style → PLATFORM_MAP key
```
**Risk zone:** Error messages containing attacker-controlled device name. No shell exposure.

### `query` (OspfQuery)
```
MCP tool call
  → Pydantic: Literal enum (neighbors|database|borders|config|interfaces|details)
  → get_action(device, "ospf", query) → PLATFORM_MAP[cli_style]["ospf"][query]
  → static CLI command string (no user input in command)
```
**Risk zone:** None — query is an enum, never interpolated.

### `vrf` (OspfQuery)
```
MCP tool call
  → Pydantic: _VRF_RE regex ^[a-zA-Z0-9_-]{1,32}$
  → get_action(device, "ospf", query, vrf=vrf)
  → _apply_vrf(command_template, vrf)
  → command_template.replace("{vrf}", vrf_name)
  → SSH command string sent to device
```
**Risk zone:** String interpolation into CLI command. This is the highest-risk data flow in netKB.
Key question: Does `_VRF_RE` reject all values that could alter command semantics?

### `query` (KBQuery)
```
MCP tool call
  → Pydantic: str, max_length=500
  → HuggingFaceEmbeddings.embed_query(query)
  → ChromaDB similarity_search(query, where=filter)
  → returns document chunks as strings
```
**Risk zone:** Embedding model abuse (long/adversarial input). No shell exposure.

### `vendor` / `topic` (KBQuery)
```
MCP tool call
  → Pydantic: Literal enums (fixed allowed values)
  → ChromaDB where-filter dict
```
**Risk zone:** None — fixed enums, no injection path.

### SSH device output
```
Device CLI response
  → Scrapli: raw text string
  → execute_command: wrapped in result dict {"output": text}
  → returned as MCP tool response
  → consumed by LLM as context
```
**Risk zone:** Prompt injection via device output. The data boundary directive in CLAUDE.md is the only control.
