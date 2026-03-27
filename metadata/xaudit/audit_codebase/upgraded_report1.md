# netKB Codebase Audit Report

**Date:** 2026-03-27
**Scope:** `server/`, `tools/`, `core/`, `transport/`, `platforms/`, `input_models/`, `ingest.py`, `testing/`
**Auditor:** Claude Opus 4.6

---

## 1. Executive Summary

The netKB codebase is well-structured with clean separation of concerns, solid Pydantic input validation, and comprehensive test coverage for its core modules. The most critical finding is the absence of a timeout on semaphore acquisition in `transport/__init__.py`, which means that if all 5 SSH slots are occupied by stalled connections, every subsequent MCP tool call blocks indefinitely -- an availability risk for a production MCP server. Across the codebase, the primary theme is **missing defensive timeouts and graceful degradation boundaries** at the transport and RAG layers.

---

## 2. Findings by Severity

### S1 -- Critical

**S1-001: No timeout on semaphore acquisition -- indefinite request blocking**

- **File:** `transport/__init__.py`, line 21
- **Description:** `async with _cmd_sem:` blocks indefinitely when all 5 semaphore slots are occupied. There is no `asyncio.wait_for()` or equivalent timeout. If 5 SSH connections stall (device unreachable but TCP handshake half-open, or Scrapli's `send_input_async` hangs past `operation_timeout_s`), every subsequent `get_ospf` or `get_interfaces` call queues behind the semaphore forever.
- **Trigger:** An LLM client issues 5 concurrent device queries to hosts that are reachable at the TCP level but unresponsive at the SSH/CLI level (e.g., control-plane overloaded routers). Scrapli's operation timeout is 30s per attempt, with 1 retry = 60s per slot worst case. A 6th request arriving during this 60s window blocks until a slot frees. If the underlying TCP connections never terminate (OS-level keepalive defaults are typically 2+ hours), the 6th and all subsequent requests block for hours.
- **Impact:** All requests to the MCP server. Once 5 slots are consumed, the server is effectively hung for all device tools. The RAG tool (`search_knowledge_base`) is unaffected since it does not acquire the semaphore.
- **Fix:** Wrap semaphore acquisition in `asyncio.wait_for()`:
  ```python
  try:
      async with asyncio.timeout(90):  # Python 3.11+; or asyncio.wait_for
          async with _cmd_sem:
              raw_output = await execute_ssh(...)
  except TimeoutError:
      return {"device": device_name, "error": "Request timed out waiting for SSH slot"}
  ```

---

### S2 -- Significant

**S2-001: Vault `get_secret` treats falsy secret values as missing**

- **File:** `core/vault.py`, line 36
- **Description:** `data.get(key) or (os.getenv(fallback_env) if fallback_env else None)` uses the `or` operator, which means a Vault secret with value `""` (empty string) or `0` will be treated as missing and the function will fall back to the env var. This is semantically incorrect -- a deliberately-empty secret in Vault should not be overridden by an env var.
- **Trigger:** An operator stores `password=""` in Vault KV (e.g., for a device with no password). `get_secret` returns the env var `ROUTER_PASSWORD` instead.
- **Impact:** Single credential resolution. Wrong credential used for SSH connection.
- **Fix:** Replace `data.get(key) or ...` with an explicit `None` check:
  ```python
  value = data.get(key)
  if value is not None:
      return value
  return os.getenv(fallback_env) if fallback_env else None
  ```

**S2-002: Retry loop holds semaphore slot during sleep**

- **File:** `transport/ssh.py`, lines 61-74; `transport/__init__.py`, line 21
- **Description:** `execute_ssh` contains a retry loop with `await asyncio.sleep(SSH_RETRY_DELAY)` (2 seconds) between attempts. This sleep occurs while the calling coroutine holds the semaphore slot (acquired in `transport/__init__.py` line 21). During the sleep, one of the 5 available SSH slots is occupied doing nothing.
- **Trigger:** A device fails on first SSH attempt with a transient error. The slot is held for 2 additional seconds during the retry delay, reducing effective concurrency to 4.
- **Impact:** Reduced throughput under load. With `SSH_RETRIES=1`, the maximum wasted time per slot is 2 seconds, which is modest. But if `SSH_RETRIES` is increased, this compounds.
- **Fix:** Release the semaphore before sleeping and re-acquire before retry, or move the semaphore acquisition into `execute_ssh` per-attempt rather than wrapping the entire call.

**S2-003: `_get_vectorstore()` is synchronous blocking called from async context**

- **File:** `tools/rag.py`, lines 19-30; called from `search_knowledge_base` at line 56
- **Description:** `_get_vectorstore()` is a synchronous function that, on first call, imports `HuggingFaceEmbeddings` and `Chroma`, downloads/loads an embedding model (potentially hundreds of MB), and initializes a ChromaDB client. This blocks the asyncio event loop for the duration of model loading. On subsequent calls it returns the cached instance immediately.
- **Trigger:** First `search_knowledge_base` call after server startup. The embedding model load can take 5-30 seconds depending on whether the model is cached on disk.
- **Impact:** All requests to the server are blocked during the first RAG query's initialization. Subsequent calls are unaffected.
- **Fix:** Run the initialization in `asyncio.to_thread()`:
  ```python
  vs = await asyncio.to_thread(_get_vectorstore)
  ```

**S2-004: `similarity_search` is synchronous blocking called from async context**

- **File:** `tools/rag.py`, line 57
- **Description:** `vs.similarity_search(params.query, **search_kwargs)` is a synchronous call that performs embedding computation and ChromaDB vector search. This blocks the event loop for the duration of each search (typically 50-200ms for the embedding step).
- **Trigger:** Every `search_knowledge_base` call.
- **Impact:** All concurrent requests are serialized through each RAG query's embedding computation.
- **Fix:** Wrap in `asyncio.to_thread()`:
  ```python
  results = await asyncio.to_thread(vs.similarity_search, params.query, **search_kwargs)
  ```

---

### S3 -- Moderate

**S3-001: Live test coverage excludes VyOS**

- **File:** `testing/live/test_platform_coverage.py`, lines 15-21
- **Description:** `TEST_DEVICES` only includes 5 devices (`D1C`, `A2A`, `C1J`, `D2B`, `A1M`). VyOS is absent. Since VyOS uses a custom Scrapli definition (`vyos_vyos.yaml`) and a different transport (`Ssh2Options`), it is the platform most likely to have runtime issues that would go undetected.
- **Trigger:** VyOS-specific bugs (definition file regex, transport negotiation) surface only in production.
- **Fix:** Add a VyOS device to `TEST_DEVICES` (requires a VyOS node in the lab topology, which TOPOLOGY.yml does not currently include).

**S3-002: No VyOS vendor docs -- `KBQuery.vendor` cannot filter VyOS content**

- **File:** `input_models/models.py`, line 49; `docs/` directory
- **Description:** `KBQuery.vendor` Literal does not include `"vyos"`. No `docs/vendor_vyos.md` file exists. VyOS-specific documentation cannot be ingested with a vendor tag or filtered by vendor. This is a completeness gap, not a bug.
- **Trigger:** User asks `search_knowledge_base` for VyOS-specific information with a vendor filter -- they cannot.
- **Fix:** Create `docs/vendor_vyos.md`, add `"vyos"` to `KBQuery.vendor` Literal, update `CLAUDE.md`.

**S3-003: `ingest.py` chunk metadata is overwritten by parent document metadata**

- **File:** `ingest.py`, lines 155-159
- **Description:** After splitting documents into chunks, line 158 does `chunk.metadata = doc.metadata.copy()`. However, `RecursiveCharacterTextSplitter.split_documents` already copies metadata to each chunk. This line overwrites the chunk metadata with the parent document's metadata, which is functionally identical in this codebase. But if the splitter ever adds chunk-specific metadata (e.g., chunk index), it would be silently lost.
- **Trigger:** No current impact. Would surface if the splitter is configured with `add_start_index=True`.
- **Fix:** Remove line 158 since `split_documents` already propagates metadata.

**S3-004: `_VAULT_FAILED` sentinel is permanently cached with no recovery path**

- **File:** `core/vault.py`, lines 7, 40
- **Description:** Once a Vault path fails, `_cache[path] = _VAULT_FAILED` is set permanently. There is no TTL, no cache invalidation, and no manual reset mechanism. If Vault is temporarily unavailable at server startup (when `settings.py` calls `get_secret`), the global credentials are resolved from env vars. If Vault later becomes available, the server must be restarted to pick up Vault secrets.
- **Trigger:** Vault is briefly unreachable during server startup, then recovers.
- **Fix:** Add a TTL or a cache eviction mechanism for the `_VAULT_FAILED` sentinel.

**S3-005: `get_action` raises raw `KeyError` for unknown category/query**

- **File:** `platforms/platform_map.py`, line 117
- **Description:** `map_entry[category][query]` raises a bare `KeyError` if `category` or `query` is not found. The callers (`tools/ospf.py` line 26, `tools/operational.py` line 20) catch `KeyError` and return an error dict, so this does not crash the server. However, the `KeyError` message is the missing key string, which does not tell the operator which lookup failed (category or query).
- **Trigger:** A new tool category is added but the platform map entry is incomplete.
- **Fix:** Raise `KeyError` with a descriptive message, e.g., `raise KeyError(f"No '{query}' in '{category}' for cli_style={device['cli_style']!r}")`.

---

### S4 -- Minor

**S4-001: `test_mcp_server.py` tests are not marked `async`**

- **File:** `testing/automated/test_mcp_server.py`, lines 5, 11
- **Description:** `test_three_tools_registered` and `test_tool_names` are `async def` methods but the class does not use `@pytest.mark.asyncio` or equivalent. With `pytest-asyncio` in auto mode these run correctly; in strict mode they would be silently skipped as "not a test" (no assertion failure, just missing coverage).
- **Trigger:** Switching `pytest-asyncio` to strict mode.
- **Fix:** Add `pytestmark = pytest.mark.asyncio` or verify `asyncio_mode = "auto"` is configured.

**S4-002: `_error_response` with empty string device includes device key**

- **File:** `tools/__init__.py`, line 6
- **Description:** `if device:` is falsy for `None` and `""`, but not for `" "` or any non-empty string. An empty-string device name would correctly be excluded, but the function description says "without device" maps to `None`. The `device` field in `OspfQuery` is a required `str`, so it could be `""`. In practice, `devices.get("")` returns `None`, producing the "Unknown device" error with `device=""` as the argument, and the resulting error dict would NOT include a `device` key (correct behavior, since `""` is falsy).
- **Trigger:** No practical impact.

**S4-003: Dead `source` variable reassignment in `ingest.py`**

- **File:** `ingest.py`, line 83 and line 106
- **Description:** `source = "NetBox"` on line 83 and `source = "NetBox"` on line 106 are in separate scopes (intent vs. inventory sections). The `source` variable from the intent section (line 83) is used on line 101 via closure, which works. But if the intent section does not set `source` (neither NetBox nor legacy file found), `source` is unbound when line 101 executes. This is dead code in that specific path because `intent_count` would be 0 and the print on line 101 would be skipped by the `if intent_count:` guard on line 100.
- **Trigger:** No practical impact due to the guard.

---

## 3. Async & Reliability Analysis

### Semaphore Behavior Under Load

The `asyncio.Semaphore(5)` at `transport/__init__.py:11` is the server's only concurrency limiter. Analysis:

- **Creation safety:** Python 3.12 (confirmed on this system) does not require a running event loop to create a `Semaphore`. Module-level creation is safe.
- **Acquisition:** Uses `async with _cmd_sem:` which guarantees release on both normal exit and exception. No manual `acquire()`/`release()` calls exist anywhere in the codebase.
- **Starvation:** No acquisition timeout exists (S1-001). Under sustained load with slow/dead devices, the semaphore can be fully exhausted. The server will continue accepting MCP requests but all device-tool responses will block indefinitely behind the semaphore.
- **Retry impact:** A retrying connection holds its slot during `asyncio.sleep(2)` (S2-002), reducing effective concurrency temporarily.

### Blocking Sync Calls in Async Context

- **`_get_vectorstore()` and `similarity_search`:** Both are synchronous and called from the async `search_knowledge_base` function (S2-003, S2-004). They block the event loop.
- **`get_secret()` in `_build_cli()`:** Called synchronously from `transport/ssh.py:31-32`. However, this runs inside the semaphore-protected section which is already awaited. The Vault call is fast (cached after first call, and first call has a 5s+10s timeout). Blocking is minimal and confined to the SSH slot holder.

### Import-Time Side Effects

- **`core/settings.py`:** Calls `get_secret()` (Vault HTTP) and `os.getenv()` at import time. This runs before `mcp.run()` starts the event loop, so blocking is acceptable.
- **`core/inventory.py`:** Calls `load_devices()` (NetBox HTTP) at import time. Same analysis -- runs before event loop.
- **`server/MCPServer.py`:** Imports all of the above at lines 16-18, then calls `mcp.run()` at line 27. All import-time blocking completes before the event loop starts.
- **Verdict:** Import-time blocking is safe for a startup-once server. Would be problematic under hot-reload.

### Lazy Initialization Race (`_get_vectorstore`)

- **`tools/rag.py:19-30`:** Checks `if _vectorstore is None`, then calls synchronous constructors (no `await`). In CPython's cooperative async model, a race requires an `await` between the None check and the assignment. There is no `await` in this path. The GIL prevents concurrent execution. **No race condition exists.**

### Connection Lifecycle

- **`async with _build_cli(device, timeout_ops) as conn:`** at `transport/ssh.py:63` guarantees `__aexit__` on both success and exception, ensuring SSH connections are closed.
- **`OpenException` bypass:** Correctly re-raised immediately at line 68, skipping the retry loop. Authentication failures do not waste retry attempts.
- **Scrapli timeout:** `operation_timeout_s=30` is set via `SessionOptions`. If `send_input_async` times out, Scrapli raises a timeout exception, which is caught by the `except Exception` at line 69 and triggers a retry (or raises after exhaustion).

### Infinite Loop Risk

- **Retry loop:** `for attempt in range(1 + SSH_RETRIES)` at `transport/ssh.py:61`. With `SSH_RETRIES=1`, this is `range(2)` -- bounded. Cannot infinite loop.
- **No `while True` loops exist anywhere in the codebase.**

---

## 4. Component Sync Status

| Contract | Status | Evidence |
|----------|--------|----------|
| Tool registrations match implementations | **PASS** | `server/MCPServer.py:22-24` registers `search_knowledge_base`, `get_ospf`, `get_interfaces`. All three import successfully from `tools.rag`, `tools.ospf`, `tools.operational`. No unregistered functions in `tools/`. |
| PLATFORM_MAP keys match all cli_style sources | **PASS** | PLATFORM_MAP keys: `ios, eos, junos, aos, routeros, vyos`. MOCK_DEVICES (`conftest.py:12-19`): R1=ios, R2=eos, R3=junos, R4=aos, R5=routeros, R6=vyos. All 6 present in both. TOPOLOGY.yml uses containerlab `kind` values (not cli_style directly); cli_style is assigned via NetBox custom fields at runtime. |
| OSPF query enum matches PLATFORM_MAP ospf subkeys (6 x 6) | **PASS** | `OspfQuery.query` Literal: `neighbors, database, borders, config, interfaces, details`. All 6 keys present under `PLATFORM_MAP[cli_style]["ospf"]` for all 6 platforms. Verified by `test_platform_map.py:TestPlatformMapStructure.test_ospf_queries_complete`. |
| Vendor Literals match ingest metadata filenames | **PASS** | `KBQuery.vendor` Literal: `cisco_ios, arista_eos, juniper_junos, aruba_aoscx, mikrotik_ros`. Files in `docs/`: `vendor_cisco_ios.md, vendor_arista_eos.md, vendor_juniper_junos.md, vendor_aruba_aoscx.md, vendor_mikrotik_ros.md`. `extract_metadata` strips the `vendor_` prefix to produce matching strings. No `vendor_vyos.md` exists (S3-002). |
| CLAUDE.md tool names and filters match code | **PASS** | CLAUDE.md lists tools `search_knowledge_base`, `get_ospf`, `get_interfaces` -- all match `MCPServer.py` registrations. Vendor filters (`cisco_ios, arista_eos, juniper_junos, aruba_aoscx, mikrotik_ros`) match `KBQuery.vendor` Literal. Topic filters (`rfc, vendor_guide, intent, inventory`) match `KBQuery.topic` Literal. Skill file `skills/ospf/SKILL.md` exists at the referenced path. |

---

## 5. Integration Point Analysis

### Vault (`core/vault.py`)

- **Unavailable at startup:** `get_secret` catches all exceptions (line 37), caches `_VAULT_FAILED`, and falls back to env vars. Server starts successfully with env var credentials. No crash.
- **Unavailable at runtime (per-connection):** `_build_cli` calls `get_secret` with `quiet=True`. Cache hit is immediate. Cache miss triggers a Vault HTTP call with `(5, 10)` timeout. On failure, falls back to global `USERNAME`/`PASSWORD` from `settings.py`. Connection proceeds.
- **Unexpected data:** `response["data"]["data"]` at line 32 will raise `KeyError` if Vault returns a non-standard response shape. This is caught by the `except Exception` handler. Graceful degradation to env var.
- **Permanent cache issue:** S3-004 -- `_VAULT_FAILED` is never cleared.

### NetBox (`core/netbox.py`, `core/inventory.py`)

- **Unavailable at startup:** `load_devices()` returns `None`. `core/inventory.py` sets `devices = {}`. Server starts with empty inventory. All device queries return `{"error": "Unknown device: ..."}`. Clean degradation.
- **Slow:** `(5, 15)` timeout on the session. `list(nb.dcim.devices.all())` could be slow with thousands of devices but is bounded by the timeout.
- **Unexpected data:** Per-device exception handling at `core/netbox.py:54` skips broken devices without crashing. Devices missing `primary_ip`, `platform`, or `cli_style` are explicitly filtered (lines 38, 46).
- **Empty result:** `load_devices()` returns `None` if no valid devices are found, triggering the empty inventory path.

### ChromaDB (`tools/rag.py`)

- **Missing data directory:** ChromaDB's `PersistentClient` creates the directory if it does not exist, resulting in an empty collection. Queries return empty results (not errors).
- **Model download failure:** `HuggingFaceEmbeddings(model_name=...)` will raise if the model cannot be loaded. This is caught by the `except Exception` at line 58, returning `{"error": "Knowledge base unavailable: ..."}`.
- **ChromaDB crash/corruption:** Same exception handler catches and returns error dict.

### Scrapli SSH (`transport/ssh.py`)

- **Device unreachable:** `OpenException` is raised and immediately re-raised (line 68). Caught by `transport/__init__.py:24-26`, returned as error dict. Clean handling.
- **Custom definition files malformed:** Scrapli loads definition files at `Cli()` construction time (inside `_build_cli`). A YAML parse error would raise during `Cli()` instantiation. This occurs inside the `async with _build_cli(...)` block, caught by the retry handler (or `except Exception` in `execute_command`). Error dict returned.
- **Stalled connection:** Scrapli's `operation_timeout_s=30` bounds `send_input_async`. After timeout + retry, the exception propagates to `execute_command` which returns an error dict. The semaphore slot is released. However, the semaphore acquisition itself has no timeout (S1-001).

---

## 6. Test Coverage Matrix

| Module | Test File | Key Gaps |
|--------|-----------|----------|
| `input_models/models.py` | `test_input_models.py` | Good coverage. Tests valid/invalid values for all 3 models, VRF injection, JSON string parsing, boundary values. |
| `platforms/platform_map.py` | `test_platform_map.py` | Good coverage. Structural completeness (all 6 x 6), VRF resolution, error cases. |
| `tools/ospf.py` | `test_tools.py` | Good coverage. Unknown device, valid multi-vendor, VRF passthrough, adversarial device names. |
| `tools/operational.py` | `test_tools.py` | Good coverage. Unknown device, valid multi-vendor. |
| `tools/rag.py` | `test_rag_pipeline.py` | Good coverage (integration test, requires populated ChromaDB). Error path tested. No unit test for `_get_vectorstore` lazy init in isolation. |
| `tools/__init__.py` | `test_tools.py` | Covered. `_error_response` with/without device. |
| `transport/__init__.py` | `test_transport.py` | Reasonable coverage. Missing: semaphore contention behavior, concurrent request handling. |
| `transport/ssh.py` | `test_ssh.py` | Good coverage. `_build_cli` per-platform construction, MikroTik `+ct`, VyOS `Ssh2Options`, Vault credential resolution, retry logic, `OpenException` bypass. |
| `core/vault.py` | `test_vault.py` | Good coverage. Cache, fallback, sentinel. Missing: test for falsy-but-valid secret values (S2-001). |
| `core/netbox.py` | `test_netbox.py` | Excellent coverage. All edge cases: missing URL/token, missing fields, per-device exceptions, intent prefix fallback, global context. |
| `core/inventory.py` | Covered indirectly via `conftest.py` mock | No dedicated test. Module-level execution tested implicitly. |
| `core/settings.py` | None | **No test file.** Settings are simple assignments. Bug class: a typo in the Vault path (e.g., `"netkb/roter"`) would silently fall back to env vars. Not currently tested. |
| `server/MCPServer.py` | `test_mcp_server.py` | Covers tool registration count and names. Missing: verifying the tool functions are the actual implementations (not just name matches). |
| `ingest.py` | `test_ingest.py` | Good coverage. `extract_metadata`, `_router_to_markdown`, `load_network_context` with NetBox/fallback paths. Missing: `ingest()` main function (chunking, embedding, storage). |
| `platforms/definitions/*.yaml` | None | **No test file.** Scrapli definition files are validated by Scrapli at runtime only. A regex error in `vyos_vyos.yaml` would surface as `OpenException` on first VyOS connection. |

---

## 7. Prioritized Recommendations

### P0 -- Fix Before Next Release

1. **Add timeout to semaphore acquisition (S1-001).** In `transport/__init__.py`, wrap `async with _cmd_sem:` in `asyncio.timeout(90)` (or a configurable value). Return an error dict on timeout. This prevents the server from hanging when all SSH slots are consumed by stalled connections.

2. **Fix falsy secret value handling (S2-001).** In `core/vault.py:36`, replace `data.get(key) or ...` with an explicit `None` check. This prevents Vault secrets with empty-string values from being silently overridden by env vars.

### P1 -- Address in Next Sprint

3. **Run `_get_vectorstore()` and `similarity_search` in a thread (S2-003, S2-004).** In `tools/rag.py`, wrap both calls in `asyncio.to_thread()`. This prevents the first RAG query from blocking the entire server during model loading, and prevents subsequent queries from blocking during embedding computation.

4. **Release semaphore during retry sleep (S2-002).** Restructure `transport/__init__.py` and `transport/ssh.py` so that the semaphore is acquired per-attempt rather than wrapping the entire retry loop. Alternatively, move the retry logic outside the semaphore context.

5. **Add VyOS to live platform coverage tests (S3-001).** Add a VyOS node to the lab topology and include it in `TEST_DEVICES`.

### P2 -- Backlog

6. **Add VyOS vendor docs and filter (S3-002).** Create `docs/vendor_vyos.md`, add `"vyos"` to `KBQuery.vendor` Literal, update `CLAUDE.md`.

7. **Add TTL to `_VAULT_FAILED` sentinel (S3-004).** Store a timestamp with the sentinel and re-attempt Vault after a configurable TTL (e.g., 5 minutes).

8. **Improve `KeyError` messages in `get_action` (S3-005).** Replace bare dict subscript with explicit checks and descriptive error messages.

9. **Remove redundant metadata reassignment in `ingest.py` (S3-003).** Delete line 158 (`chunk.metadata = doc.metadata.copy()`).

10. **Add `core/settings.py` unit test.** Test that the Vault path string and env var names are correct, guarding against typos.
