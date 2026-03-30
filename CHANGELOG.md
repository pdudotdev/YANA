# Changelog

## v1.2.0 — 2026-03-30

Removed Vault and NetBox, implemented RAG optimizations, standardized on JUnit XML for test results, added Makefile for setup.

### Vault and NetBox Removal

- **Deleted** `core/vault.py` and `core/netbox.py` — Vault and NetBox are production concerns, unnecessary for QA/lab networks.
- **Deleted** `testing/automated/test_vault.py` and `testing/automated/test_netbox.py`.
- **Moved** `core/legacy/NETWORK.json` → `data/NETWORK.json` and `core/legacy/INTENT.json` → `data/INTENT.json` — JSON is the primary (and only) data source, not a "legacy" fallback.
- **Simplified `core/settings.py`** — credentials read directly from `ROUTER_USERNAME` / `ROUTER_PASSWORD` env vars.
- **Simplified `core/inventory.py`** — JSON-only loading from `data/NETWORK.json`, no NetBox fallback.
- **Simplified `tools/intent.py`** — JSON-only loading from `data/INTENT.json`, no NetBox fallback.
- **Simplified `tools/status.py`** — reports 3 fields: inventory, intent, chromadb (removed vault).
- **Simplified `transport/ssh.py`** — global credentials only (no per-vendor Vault lookup).
- **Removed dependencies** from `requirements.txt`: `hvac`, `pynetbox`, `ncclient`, `ansible-core`.

### RAG Optimizations

- **Protocol metadata field** — every chunk tagged with `protocol` (ospf, bgp, eigrp, general) during ingestion. Filterable at query time via `search_knowledge_base(protocol="ospf")`. Eliminates cross-protocol noise as the corpus grows.
- **Contextual chunk headers** — `[Source: filename | Protocol: protocol]` prepended to each chunk during ingestion, improving embedding quality and vector placement.
- **Collection renamed** — `ospf_kb` → `network_kb` (generic, multi-protocol ready).
- **`KBQuery` model** — added `protocol` field (`Literal["ospf", "bgp", "eigrp"] | None`).
- See [OPTIMIZATIONS.md](metadata/scalability/OPTIMIZATIONS.md) for the full optimization roadmap.

### JUnit XML for Test Results

- **`results/` directory** — test results now live at project root (was `ansible/results/`). Any test framework that outputs JUnit XML is supported.
- **Ansible JUnit template** — `ansible/templates/junit_results.xml.j2` renders qa_results as JUnit XML with `<properties>` for device, rfc_ref, description, rfc_citation.
- **Ansible playbook updated** — `network_qa.yml` writes JUnit XML to `results/results_<timestamp>.xml`.
- **Ansible inventory** — switched from Vault lookups to env var lookups (`ROUTER_USERNAME`, `ROUTER_PASSWORD`, `ROUTER_PASSWORD_JUNOS`). Removed `community.hashi_vault` from collection requirements.

### `/qa` Skill Rewrite

- Rewritten for JUnit XML parsing (was JSON). Loads `.xml` files from `results/`, parses `<testcase>` elements with `<properties>` and `<failure>` children.
- Framework-agnostic — works with results from pytest, pyATS, Robot Framework, Ansible, or any JUnit XML producer.

### Makefile

- Four targets: `make install` (venv + deps), `make ingest` (rebuild ChromaDB), `make clean` (reset), `make setup` (both).

### Documentation

- **README.md** — complete rewrite as "Network QA Investigation Tool." Removed all Vault/NetBox references. Added Customization, QA Workflow, and Knowledge Base sections.
- **CLAUDE.md** — reframed as investigation tool. Removed vault from status table, added protocol filter to KB search, updated tool descriptions.
- **WORKFLOW.md** — complete rewrite. Removed Vault/NetBox references. Documents JSON-only data sources, env var credentials, protocol metadata, JUnit XML results.
- **OPTIMIZATIONS.md** — updated current architecture table (collection name, chunk count, protocol metadata, contextual headers). Marked items 1 and 5 as implemented.
- **`.env.example`** — new file with `ROUTER_USERNAME`, `ROUTER_PASSWORD`, `SSH_STRICT_HOST_KEY`.

---

## v1.0.0 — 2026-03-24

Initial release. RAG-powered OSPF knowledge base assistant for multi-vendor networks.

### MCP Server

- FastMCP server (`server/MCPServer.py`) exposing 7 read-only tools
- **`search_knowledge_base`** — vector similarity search over OSPF documentation stored in ChromaDB. Supports metadata filtering by vendor (`cisco_ios`, `arista_eos`, `juniper_junos`, `aruba_aoscx`, `mikrotik_ros`) and topic (`rfc`, `vendor_guide`). Compound filters supported via ChromaDB `$and` operator.
- **`get_ospf`** — queries OSPF operational data from live devices via SSH. 6 query types: `neighbors`, `database`, `borders`, `config`, `interfaces`, `details`. Commands resolved automatically per vendor through the platform map.
- **`get_interfaces`** — queries interface status and IP information from live devices via SSH. Vendor-specific command resolved through the platform map.

### RAG Pipeline

- **Ingestion** (`ingest.py`) — loads OSPF documentation from `docs/` (RFCs + vendor guides). Documents are chunked with LangChain `RecursiveCharacterTextSplitter` (800 char chunks, 100 char overlap), embedded locally with `all-MiniLM-L6-v2` (384-dim vectors), and stored in ChromaDB. Device inventory and network intent are **not** stored in ChromaDB — they are served at query time from NetBox (with `core/legacy/NETWORK.json` and `core/legacy/INTENT.json` as static fallbacks).
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

### Testing (17 suites, 146 test functions)

- **15 unit test suites** (UT-001 through UT-015):
  - Input model validation — query types, VRF injection, vendor/topic literals, bounds
  - Platform map — structure completeness, VRF resolution, vendor coverage
  - Tool layer — unknown device handling, mock SSH, VRF passthrough
  - Transport dispatcher — error wrapping, result structure
  - Vault client — caching, fallback, sentinel behavior
  - Ingest helpers — metadata extraction, markdown conversion
  - NetBox loader — device mapping, intent loading, error handling
  - SSH layer — retry logic, vendor-specific options
  - MCP server registration — all 7 tools registered and importable
  - Inventory loader — NetBox primary, JSON fallback, empty fallback
  - List devices tool — filtering, empty inventory handling
  - Status tool — all 4 subsystem probes
  - Routing tool — command resolution, VRF passthrough
  - Intent tool — NetBox primary, JSON fallback
  - Security controls — VRF injection patterns, valid VRF acceptance
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
- `metadata/workflow/workflow.md` — end-to-end RAG pipeline walkthrough with real data (actual chunks, vectors, similarity scores from the live ChromaDB)

---

## Updates — 2026-03-28

### Routing Skill

- **`skills/routing/SKILL.md`** — new Routing Policy & Path Selection skill. Covers the full path-selection investigation sequence: longest-prefix-match override check (Step 0), PBR three-query chain (policy_based_routing → route_maps → access_lists), route filtering at redistribution points (distribute-list interaction with LSDB), ECMP/CEF per-destination hashing, AD conflict table (Connected 0, Static 1, eBGP 20, OSPF 110, iBGP 200). Prerequisite gate enforces interface and neighbor health before any policy investigation.
- Adapted from aiNOC routing skill with all tool references remapped to YANA's `get_routing` API. NAT/PAT section replaced with advisory note. Redistribution query replaced by `get_ospf(device, "config")`. All `get_bgp` and `traceroute` references removed or noted as out-of-scope.

### Traceroute Tool

- **`traceroute`** MCP tool added — traces the forwarding path from a device to a destination IP. Supports optional `source` parameter to force probe source address. Uses `SSH_TIMEOUT_OPS_LONG = 90s` to accommodate multi-hop paths with per-hop timeouts.
- **Platform map `tools` category** — `traceroute` command added for all 6 CLI styles. VRF-aware via `{default/vrf}` dict pattern. IOS uses `traceroute ip vrf {vrf}` (avoids extended interactive prompt). JunOS uses `traceroute routing-instance {vrf}`. RouterOS uses `/tool/traceroute count=1` (terminates after one probe per hop rather than running continuously). AOS-CX uses plain `traceroute` (no VRF keyword supported for traceroute).
- **`SSH_TIMEOUT_OPS_LONG = 90`** added to `core/settings.py`.
- **`TracerouteInput`** Pydantic model added to `input_models/models.py` — `device`, `destination`, optional `source`, optional `vrf` (VRF regex validation inherited from `BaseParamsModel`).
- Registered in `server/MCPServer.py` — MCP tool count increased from 7 to 8.

### Platform Map Fixes

- **IOS traceroute VRF template** — changed from `traceroute vrf {vrf}` to `traceroute ip vrf {vrf}`. The `ip` protocol keyword forces inline (non-interactive) execution on IOS/IOL; without it the CLI enters extended traceroute interactive mode and the SSH session times out.
- **`_apply_vrf()` "default" VRF handling** — VRF name `"default"` (case-insensitive) is now treated as no VRF, using the default command variant. `"default"` denotes the global routing table; no vendor accepts it as an explicit VRF argument in traceroute or other commands.
- **RouterOS traceroute** — `count=1` parameter added. MikroTik's `/tool/traceroute` sends continuous probes indefinitely by default; `count=1` limits it to one probe per hop so the command terminates.
- **JunOS Evolved routing commands** — `route_maps` command corrected from `show policy-options policy-statement` to `show configuration policy-options policy-statement`; `prefix_lists` corrected from `show policy-options prefix-list` to `show configuration policy-options prefix-list`. The `show policy-options` path is a configuration hierarchy, not a valid operational mode command on JunOS Evolved.

### CLAUDE.md — Workflow Guidance

- Routing skill added to Step 1 skill table.
- Skill selection guidance added: OSPF skill for protocol adjacency/LSDB issues; routing skill for path selection, PBR, route filtering, ECMP, AD conflicts.
- Reachability guidance added: when the complaint is end-to-end reachability, start with `traceroute` to localize the breaking hop before loading any protocol skill.
- `traceroute` added to Step 3 tool table.

### Testing

- **LT-001** expanded from 35 to 65 tests: added `routing_table` (5 queries × 5 devices = 25 tests) and `traceroute` (1 × 5 devices = 5 tests). Traceroute destination fixed to `172.20.20.207` (C1J management IP, reachable from all vendors).
- **UT-002** (Platform Map) — `TestTracerouteVrf` class added (7 tests covering VRF resolution per vendor, RouterOS no-VRF behavior, IOS `ip vrf` syntax). `TestApplyVrf` extended with 3 tests for `"default"` VRF normalization (case-insensitive).
- **UT-003** (Tool Layer) — `TestTraceroute` class added (5 tests: unknown device, IOS command structure, IOS source syntax, EOS VRF passthrough, RouterOS `address=`/`src-address=` syntax).
- **UT-009** (MCP Server) — updated to assert 8 tools; `"traceroute"` added to expected names set.
- **UT-001** (Input Models) — `TestTracerouteInput` class added (5 tests: minimal, full, VRF injection, JSON parsing, missing destination).
- **UT-015** (Security Controls) — `TracerouteInput` VRF injection tests added (18 injection patterns blocked, 6 valid VRF names accepted).

---

## v1.1.0 — 2026-03-29

### Ansible QA Framework

- **Network QA playbooks** — new Ansible-based health check framework in `ansible/`. Entry point `playbooks/network_qa.yml` discovers test cases from `ansible/test_cases/*.yml`, runs each via `_run_check.yml`, and writes results to `ansible/results/results_<timestamp>.json`.
- **NETCONF transport** — test checks query device state over NETCONF using the `ietf-routing` YANG model (`urn:ietf:params:xml:ns:yang:ietf-routing`) for VRF routing table reads. Credentials sourced from HashiCorp Vault via `community.hashi_vault` Ansible collection.
- **Read-only test design** — replaced 3 fault-injection test cases (config push, convergence wait, teardown) with a single read-only routing table assertion. No configuration is pushed to devices.
- **`route_exists` filter** (`ansible/filter_plugins/ospf_filters.py`) — Jinja2 filter that parses NETCONF XML and checks for a destination prefix in the routing table.
- **Test case format** — declarative YAML defining device, VRF, assertion, and RFC reference. Example: `route_to_a2a.yml` verifies E1C has a route to A2A's loopback (192.168.42.1) in VRF1.
- **ncclient device handler fix** — added `vars:` binding for `ansible_netconf_ncclient_device_handler` in the netcommon NETCONF plugin so inventory variables are read correctly (forces `iosxe` handler instead of `default`).

### `/qa` Skill

- **Generic investigation skill** (`.claude/skills/qa/SKILL.md`) — rewritten to be device- and test-agnostic. Loads latest results JSON, triages pass/fail, presents numbered failure list, user picks a failure to investigate, agent runs full diagnostic workflow (intent → live state → skill decision trees → KB search), reports findings, then re-presents remaining failures for the next pick.
- **Shared root cause detection** — after investigating a failure, if its root cause likely explains other failures on the list, the agent says so — user can skip those.

### Documentation

- **`WORKFLOW.md`** — complete rewrite covering both operational modes: interactive troubleshooting (user asks questions) and automated QA (Ansible health checks + `/qa` skill). Includes tool table, SSH pipeline diagram, RAG pipeline explanation, step-by-step walkthroughs for both modes, concrete examples, and ASCII architecture diagram.
- **`README.md`** — added QA & Ansible section with prerequisites, running instructions, and `/qa` skill usage. Updated project structure to reflect `ansible/` directory layout.

### Test Cleanup

- **269 → 169 tests** (37% reduction) — removed tests that verify Pydantic builtins, duplicate error paths, or Python language features rather than project logic.
- Gutted `test_input_models.py` to 2 tests (JSON string parsing only — the custom `@model_validator`).
- Trimmed `test_security.py` to OspfQuery variants only (same VRF regex shared across all models).
- Removed trivial tests from `test_status.py` (Path.exists, enum string checks), `test_tools.py` (2-line dict builder, duplicate unknown_device), `test_transport.py` (duplicate SSH error), `test_list_devices.py` (duplicate filter), `test_ingest.py` (duplicate RFC), `test_mcp_server.py` (count implied by name check), `test_inventory.py` (fixture-testing, not production code).

### Housekeeping

- **`.gitignore`** — added `ansible/collections/ansible_collections/` and `ansible/results/` to prevent installed collections and ephemeral result files from being committed.
- Old fault-injection test cases moved to `core/legacy/`.
