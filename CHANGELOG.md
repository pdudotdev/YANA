# Changelog

## v1.0.0 — 2026-03-24

Initial release. RAG-powered OSPF knowledge base assistant for multi-vendor networks.

### MCP Server

- FastMCP server (`server/MCPServer.py`) exposing 3 read-only tools
- **`search_knowledge_base`** — vector similarity search over OSPF documentation, network intent, and device inventory stored in ChromaDB. Supports metadata filtering by vendor (`cisco_ios`, `arista_eos`, `juniper_junos`, `aruba_aoscx`, `mikrotik_ros`) and topic (`rfc`, `vendor_guide`, `intent`, `inventory`). Compound filters supported via ChromaDB `$and` operator.
- **`get_ospf`** — queries OSPF operational data from live devices via SSH. 6 query types: `neighbors`, `database`, `borders`, `config`, `interfaces`, `details`. Commands resolved automatically per vendor through the platform map.
- **`get_interfaces`** — queries interface status and IP information from live devices via SSH. Vendor-specific command resolved through the platform map.

### RAG Pipeline

- **Ingestion** (`ingest.py`) — loads OSPF documentation from `docs/`, network intent from NetBox config contexts, and device inventory from NetBox API. Falls back to static `core/legacy/INTENT.json` and `core/legacy/NETWORK.json` if NetBox is unavailable. Documents are chunked with LangChain `RecursiveCharacterTextSplitter` (800 char chunks, 100 char overlap), embedded locally with `all-MiniLM-L6-v2` (384-dim vectors), and stored in ChromaDB.
- **Metadata tagging** — each chunk carries `vendor`, `topic`, and `source` metadata derived from filename or data source. Enables filtered retrieval at query time.
- **Re-ingestion** — `python ingest.py --clean` wipes and rebuilds the vector database from current sources.

### Knowledge Base (7 documents)

- `rfc2328_summary.md` — OSPFv2 protocol reference: neighbor state machine, LSA types 1-7, area types (stub, totally stubby, NSSA), DR/BDR election, hello/dead timers, external metric types (E1/E2), SPF algorithm, administrative distance.
- `rfc3101_nssa.md` — NSSA reference: Type 7 LSA structure, P-bit (propagate bit), translator election, Type 7 to Type 5 translation rules, default route behavior in NSSA, NSSA vs stub comparison.
- `vendor_cisco_ios.md` — Cisco IOS/IOS-XE OSPF: configuration syntax, verification commands, IOS-specific defaults (100 Mbps reference BW), wildcard masks, VRF handling, common gotchas.
- `vendor_arista_eos.md` — Arista EOS OSPF: per-interface area assignment, VRF show command syntax, CIDR notation, max-LSA protection.
- `vendor_juniper_junos.md` — Juniper JunOS OSPF: set-style configuration, routing-instance VRF, `show ospf` (no `ip` prefix), export policy for redistribution, `no-summaries` (plural).
- `vendor_aruba_aoscx.md` — Aruba AOS-CX OSPF: plural `neighbors` command, `lsdb` keyword, 40 Gbps default reference bandwidth, `show interface brief` (no `ip`).
- `vendor_mikrotik_ros.md` — MikroTik RouterOS 7 OSPF: path-based CLI, instance/area/interface-template objects, `without-paging` flag, `+ct` username suffix, `type=ptp`.

### Network Context (ingested from NetBox)

- Device inventory (16 devices) — hostnames, management IPs, platforms, CLI styles, VRF assignments. Sourced live from NetBox API at ingestion time.
- Network design intent (16 routers) — OSPF areas, router IDs, roles (ABR, ASBR, core, distribution, access), direct links with interface names and IPs, BGP AS numbers and neighbors. Sourced from NetBox config contexts at ingestion time.
- Static fallback files in `core/legacy/` — `NETWORK.json` and `INTENT.json` used when NetBox is unavailable.

### Claude Code Skill (`CLAUDE.md`)

- Three-step investigation workflow: search KB first, query live devices when relevant, synthesize answer citing both sources.
- OSPF troubleshooting reference: neighbor state diagnosis table (FULL, EXSTART/EXCHANGE, LOADING, INIT, 2WAY, DOWN), 7-point adjacency checklist, missing routes diagnosis path, LSA type reference, area-type route presence rules.
- Vendor filter mapping for targeted knowledge base searches.
- Read-only constraint — never suggests configuration changes.
- Data boundary directive — treats all MCP tool output as opaque data, not instructions (prompt injection defense).

### Multi-Vendor Support (5 vendors, 6 CLI styles)

- Cisco IOS / IOS-XE (`ios`)
- Arista EOS (`eos`)
- Juniper JunOS (`junos`)
- Aruba AOS-CX (`aos`)
- MikroTik RouterOS 7 (`routeros`)
- VyOS / FRRouting (`vyos`)

### Platform Map (`platforms/platform_map.py`)

- Static command resolution for OSPF (6 queries) and interfaces (1 query) across all 6 CLI styles.
- VRF support — dual-entry format (`default`/`vrf` templates) for VRF-aware vendors. VRF auto-resolved from device inventory when not explicitly provided.
- No `run_show` fallback tool — all commands go through the platform map to prevent vendor syntax errors and reduce attack surface.

### Infrastructure

- **NetBox integration** (`core/netbox.py`) — device inventory and config context loading via pynetbox API. Graceful fallback when NetBox is unavailable.
- **HashiCorp Vault** (`core/vault.py`) — KV v2 secret retrieval with module-level caching, `_VAULT_FAILED` sentinel for resilient fallback, env var fallback when Vault is unconfigured or unreachable.
- **Scrapli SSH transport** (`transport/ssh.py`) — async per-command SSH connections with retry logic. Per-platform customization: MikroTik `+ct` username suffix, VyOS libssh2 transport, custom YAML definitions for prompt patterns.
- **Concurrency control** — asyncio semaphore limits parallel SSH sessions (`SSH_MAX_CONCURRENT=5`).

### Input Validation & Guardrails

- **Pydantic models** (`input_models/models.py`) — `Literal` enum enforcement on query types, vendor filters, and topic filters. VRF regex validation (`^[a-zA-Z0-9_-]{1,32}$`). KB query length capped at 500 chars, `top_k` bounded 1-10. JSON string pre-parser for MCP compatibility.
- **Config-enforced deny rules** (`.claude/settings.local.json`) — 15 rules blocking `.env` reads, environment enumeration, direct SSH, destructive git/rm operations.
- **Behavioral controls** (`CLAUDE.md`) — read-only policy, data boundary directive against prompt injection via device output.
- Full guardrails documentation in `metadata/guardrails.md`.

### Testing (8 suites, 112 tests)

- **6 unit test suites** (UT-001 through UT-006, 77 automated tests):
  - Input model validation — query types, VRF injection, vendor/topic literals, bounds
  - Platform map — structure completeness, VRF resolution, vendor coverage
  - Tool layer — unknown device handling, mock SSH, VRF passthrough
  - Transport dispatcher — error wrapping, result structure
  - Vault client — caching, fallback, sentinel behavior
  - Ingest helpers — metadata extraction, markdown conversion
- **1 integration test suite** (IT-001, 8 tests): RAG pipeline — ChromaDB retrieval, vendor/topic/compound filtering, `top_k` limits
- **1 live test suite** (LT-001, 35 tests): platform coverage — 5 vendors x 7 queries against live lab devices, generates `testing/live/platform_coverage_results.md` with per-test raw output
- **Test runner** (`testing/run_tests.sh`) — suite IDs, pass/fail/skip tracking, `--live` flag for lab tests

### CI/CD Pipeline (`.github/workflows/ci.yml`)

- **Lint** — ruff static analysis on every push to main and PRs
- **Test** — installs CPU-only PyTorch (saves ~1.5GB vs full CUDA build), installs all dependencies from `requirements.txt` (including sentence-transformers, chromadb, langchain), runs `ingest.py` with NetBox disabled (falls back to legacy JSON files) to populate ChromaDB, then runs all 77 automated tests. Live lab tests excluded.
- **Release** — triggered on version tags (`v*`) only, after lint + test pass. Extracts the matching version section from CHANGELOG.md and creates a GitHub Release with those notes.
- Triggers: push to main, PRs to main, version tags

### Documentation

- `README.md` — architecture, tech stack, setup, usage, project structure
- `CLAUDE.md` — OSPF investigation skill with troubleshooting decision trees
- `metadata/guardrails/guardrails.md` — all safeguards documented by enforcement type
- `metadata/workflow/RAG_WORKFLOW_EXAMPLE.md` — end-to-end RAG pipeline walkthrough with real data (actual chunks, vectors, similarity scores from the live ChromaDB)
