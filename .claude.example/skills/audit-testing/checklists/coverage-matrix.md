# Coverage Matrix — YANAA

Use this during Phase 5. The table below is a pre-built starting point based on the known codebase structure. Verify it is still accurate (files exist, mappings are correct), then fill in the "Functions Tested" and "Functions NOT Tested" columns based on your reading of the test files.

---

## Source Module → Test File Mapping

| Source Module | Test File | Key Functions to Verify |
|---------------|-----------|------------------------|
| `core/settings.py` | **NONE** | `SSH_TIMEOUT_OPS`, `SSH_RETRIES`, `SSH_MAX_CONCURRENT`, `USERNAME`, `PASSWORD` load path |
| `core/vault.py` | `test_vault.py` | `get_secret()`, `_cache` behavior, `_VAULT_FAILED` sentinel caching, env var fallback |
| `core/netbox.py` | `test_netbox.py` | `load_devices()`, `load_intent()`, error paths (missing primary_ip, missing cli_style) |
| `core/inventory.py` | **NONE** (indirect via conftest) | `devices` dict, import-time `load_devices()` call |
| `transport/__init__.py` | `test_transport.py` | `execute_command()`, `_cmd_sem` semaphore behavior |
| `transport/ssh.py` | `test_ssh.py` | `_build_cli()`, `execute_ssh()`, retry logic, `OpenException` handling |
| `platforms/platform_map.py` | `test_platform_map.py` | `PLATFORM_MAP` structure, `_apply_vrf()`, `get_action()` |
| `input_models/models.py` | `test_input_models.py` | `OspfQuery`, `InterfacesQuery`, `KBQuery`, `BaseParamsModel.parse_string_input` |
| `tools/__init__.py` | `test_tools.py` | `_error_response()` |
| `tools/ospf.py` | `test_tools.py` | `get_ospf()` |
| `tools/operational.py` | `test_tools.py` | `get_interfaces()` |
| `tools/rag.py` | `test_rag_pipeline.py` *(IT, conditionally skipped)* | `search_knowledge_base()`, `_get_vectorstore()` |
| `server/MCPServer.py` | `test_mcp_server.py` | Tool registration (count and names only — NOT functionality) |
| `ingest.py` | `test_ingest.py` | `extract_metadata()`, `_router_to_markdown()` — main `ingest()` NOT tested |

---

## Modules with No Test File

These modules have zero direct test coverage. For each, note what class of bug could hide undetected:

| Module | Why this is risky |
|--------|------------------|
| `core/settings.py` | Import-time Vault calls and env var fallback logic. A misconfiguration here affects every tool invocation. |
| `core/inventory.py` | Import-time side effect: calls `load_devices()`. If this fails, the server has empty inventory. No test verifies the startup behavior under NetBox failure. |

---

## Known Partial Coverage

| Module | Tested | NOT Tested |
|--------|--------|------------|
| `ingest.py` | `extract_metadata()`, `_router_to_markdown()` | Main `ingest()` function: chunking, embedding, ChromaDB write, error handling |
| `server/MCPServer.py` | Tool registration count and names | Tool invocation through FastMCP protocol, server startup, error middleware |
| `tools/rag.py` | `search_knowledge_base()` (IT-001, skipped without ChromaDB) | `_get_vectorstore()` lazy init, race condition scenario, ChromaDB missing dir |
| `transport/__init__.py` | `execute_command()` error paths | Semaphore behavior under concurrent load, slot exhaustion scenario |

---

## Live Test Coverage

Live tests (`testing/live/test_platform_coverage.py`) cover:

| Device | Platform | OSPF queries | Interfaces |
|--------|----------|-------------|------------|
| D1C | ios | all 6 | yes |
| A2A | eos | all 6 | yes |
| C1J | junos | all 6 | yes |
| D2B | aos | all 6 | yes |
| A1M | routeros | all 6 | yes |
| **VyOS** | **vyos** | **NONE** | **NONE** |

VyOS is in `PLATFORM_MAP` and in `MOCK_DEVICES` but has **no live test coverage**. Determine whether this is intentional (no VyOS device in the lab) or a gap.

---

## Mutation Thinking Template

For each coverage gap, complete this:

> "If I changed [specific line/condition] in [module] to [wrong value/behavior], which test would catch it?"
>
> If the answer is "none," this is a **critical gap (S3)**.

Examples of bugs that would currently go undetected:
- `core/settings.py` misconfigured `SSH_RETRIES = -1` → `last_exc` is `None` → `raise None` → `TypeError` at runtime
- `core/inventory.py` import-time failure → server starts with empty `devices` dict → all device queries silently return "not found"
- `ingest.py::ingest()` fails to write to ChromaDB → no error raised → KB is empty → all search results are empty

Fill in your own entries as you discover additional gaps.
