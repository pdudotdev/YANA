# YANA Test Quality Audit Report

**Date:** 2026-03-27
**Auditor:** External Senior QA Architect
**Scope:** All automated, live, and manual tests under `testing/`, CI pipeline, source modules

---

## 1. Executive Summary

The YANA test suite is **structurally sound** — it covers the major functional paths, has good input validation tests, and demonstrates awareness of security guardrails. However, the suite contains **no ghost passes (S1)** upon rigorous analysis, but does contain **two mock fidelity issues (S2)** that reduce confidence in specific tests, **several meaningful coverage gaps (S3)** in critical modules (`core/settings.py`, `core/inventory.py`, main `ingest()` pipeline, concurrency behavior), and **a few test infrastructure concerns (S4)** in `run_tests.sh` that could mask failures. The most critical theme is that **import-time side effects in `core/settings.py` and `core/inventory.py` are completely untested**, meaning a misconfiguration that breaks the server at startup would go undetected by CI.

---

## 2. Verdict Summary Table

| Suite ID | Suite Name | Test Count | Verdict |
|----------|-----------|------------|---------|
| UT-001 | Input Model Validation | 14 | **EXCELLENT** |
| UT-002 | Platform Map | 12 | **EXCELLENT** |
| UT-003 | Tool Layer | 11 | **SOLID** |
| UT-004 | Transport Dispatcher | 5 | **SOLID** |
| UT-005 | Vault Client | 5 | **GOOD** |
| UT-006 | Ingest Helpers | 9 | **GOOD** |
| UT-007 | NetBox Loader | 12 | **EXCELLENT** |
| UT-008 | SSH Layer | 8 | **SOLID** |
| UT-009 | MCP Server Registration | 2 | **MINIMAL** |
| IT-001 | RAG Pipeline | 8 | **CONDITIONAL** |
| LT-001 | Platform Coverage | 35 | **SOLID** |
| MT-001 | Manual Tests | 10 | **GOOD** |

---

## 3. Ghost Conditions and Silent Passes (S1)

After rigorous analysis applying the ghost-pass checklist to every test, **no S1 findings were identified**. Each test was evaluated against the six-question checklist:

**Tests that were closely examined and cleared:**

1. **`test_tools.py::TestGetOspf::test_valid_device_ios` (line 29-37):** This test patches `transport.execute_ssh` with a mock return value, then asserts `result["_command"]` contains the expected command and `result["raw"]` contains mock output. While the raw value assertion checks mock output (Q4 concern), the `_command` assertion verifies that `get_ospf()` correctly resolved the platform-map command via `get_action()` — this is the function's core logic. If `get_ospf()` were replaced with `pass`, the assertion `result["device"] == "R1"` would fail because `result` would be `None`. **Not a ghost pass.**

2. **`test_transport.py::TestExecuteCommand::test_success_returns_structured_dict` (line 12-20):** Similar pattern — mock SSH return value flows into `result["raw"]`, but the test also verifies `result["device"]`, `result["cli_style"]`, and `result["_command"]`, which are constructed by `execute_command()` itself, not the mock. **Not a ghost pass.**

3. **`test_ssh.py::TestBuildCli::test_standard_device_uses_binoptions` (line 53-58):** Uses `mock_bin.assert_called_once()` — this is a Q3 concern (assert on mock state). However, the test's purpose is specifically to verify that `_build_cli` calls `BinOptions` for standard devices (as opposed to `TransportSsh2Options` for VyOS), which is a legitimate integration verification. If `_build_cli` were replaced with `pass`, the assertion would fail. **Not a ghost pass.**

4. **`test_ssh.py::TestBuildCli::test_vyos_uses_ssh2options` (line 60-65):** Same pattern as above. Verifies VyOS path selection. `assert_called_once()` would fail if `_build_cli` did not call `TransportSsh2Options`. **Not a ghost pass.**

5. **`test_vault.py::TestVault::test_vault_failure_sets_sentinel` (line 54-68):** The mock `hvac.Client` raises an exception. The test asserts both the return value (`== "env_value"`) and the sentinel state (`_cache["fail/path"] is _VAULT_FAILED`). The sentinel check verifies internal state produced by `get_secret()` logic. If `get_secret()` were `pass`, it would return `None`, failing the `== "env_value"` assertion. **Not a ghost pass.**

---

## 4. Mock Fidelity Analysis (S2)

### Finding S2-001: `test_ssh.py` — `_build_cli` mock return shape inconsistent with real `Cli`

**File:** `testing/automated/test_ssh.py`, lines 14-21 (`_async_cm` helper)

**Mock shape:** `_async_cm()` returns a `MagicMock` configured as an async context manager. `mock_conn.send_input_async.return_value = MagicMock(result=raw_result)`.

**Real function:** `transport/ssh.py` line 63-66: `_build_cli()` returns a `scrapli.Cli` object. When used as `async with _build_cli(...) as conn:`, `conn.send_input_async(input_=command)` returns a `scrapli.response.Response` object whose `.result` attribute is a string.

**Structural difference:** The mock's `send_input_async` is called without `input_=` keyword in the mock setup, whereas the real code calls `conn.send_input_async(input_=command)`. This is not a fidelity issue because `AsyncMock` accepts any arguments. The actual return value shape (`MagicMock(result=raw_result)`) matches the real `Response.result` attribute access pattern. **Conclusion: The mock is structurally compatible.** However, the mock does not verify that `input_=command` is passed correctly — `send_input_async` would accept any arguments. This means a bug that sends the wrong command string (e.g., empty string, wrong variable) would not be caught.

**Severity:** S2 (low impact — the command dispatch is tested elsewhere in UT-003)

**Fix:** Add `mock_conn.send_input_async.assert_called_once_with(input_="show ip ospf neighbor")` in `test_success_returns_raw_string`.

---

### Finding S2-002: `test_vault.py::test_vault_failure_sets_sentinel` — Mock `hvac` module structure

**File:** `testing/automated/test_vault.py`, lines 62-64

**Mock shape:** `patch.dict("sys.modules", {"hvac": MagicMock()})` followed by `import hvac; hvac.Client.return_value.secrets.kv.v2.read_secret_version.side_effect = Exception("unreachable")`.

**Real function:** `core/vault.py` line 27: `client = hvac.Client(url=vault_addr, token=vault_token)`, then `client.session.timeout = (5, 10)`, then `client.secrets.kv.v2.read_secret_version(path=path, ...)`.

**Structural difference:** The real code sets `client.session.timeout = (5, 10)` on the client instance. The mock `MagicMock()` silently accepts this attribute assignment. But the mock `hvac` in `sys.modules` is separate from the import inside `core/vault.get_secret`. The test imports `hvac` at the test level and configures the side_effect there, but `get_secret()` does its own `import hvac` and `hvac.Client(...)`. Since `sys.modules["hvac"]` is patched, both imports resolve to the same `MagicMock`. The `hvac.Client.return_value` mock chain works because `MagicMock().__call__()` returns `MagicMock.return_value`, which is what `.secrets.kv.v2.read_secret_version.side_effect` is set on.

**Conclusion:** The mock structure is **functionally correct** for the exception path being tested. The `side_effect = Exception(...)` will trigger, the exception handler in `get_secret()` will set the sentinel, and the test assertions will verify that. The mock does not fully replicate the `session.timeout` assignment path but this is irrelevant to the exception-path test.

**Severity:** S2 (minimal — the mock is adequate for the specific path being tested, but does not cover the happy-path response structure `response["data"]["data"]`)

**Fix:** Add a separate happy-path test that mocks `read_secret_version` to return `{"data": {"data": {"username": "admin", "password": "secret"}}}` and verifies `get_secret("path", "username") == "admin"`. This tests the real response parsing logic.

---

## 5. Coverage Gap Inventory

### HIGH Priority

#### S3-001: `core/settings.py` — Zero test coverage

**Source:** `core/settings.py` (14 lines)
**Test file:** None

This module runs Vault calls at import time to resolve `USERNAME` and `PASSWORD`. It also defines `SSH_TIMEOUT_OPS`, `SSH_RETRIES`, `SSH_RETRY_DELAY`, `SSH_MAX_CONCURRENT`, and `SSH_STRICT_HOST_KEY`. These values flow into every SSH connection. There is no test that verifies:
- `get_secret()` is called with the correct path/key/fallback for username and password
- The `SSH_STRICT_HOST_KEY` env var parsing (`"true"`, `"1"`, `"yes"` accepted; others rejected)
- The default values are as documented

**Bug class:** A typo in the Vault path (`"yana/roter"` instead of `"yana/router"`) would cause all SSH connections to use env-var fallback credentials. A change to `SSH_STRICT_HOST_KEY` parsing logic (e.g., inverting the condition) would disable host key verification silently. Neither would be caught by any test.

#### S3-002: `core/inventory.py` — Import-time behavior untested

**Source:** `core/inventory.py` (15 lines)
**Test file:** None (indirectly mocked via `conftest.py`)

The `conftest.py` fixture patches `core.inventory.devices` with `MOCK_DEVICES`, bypassing the entire import-time `load_devices()` call. No test verifies:
- What happens when `load_devices()` returns `None` at import time (the `devices: dict = {}` fallback)
- That the log error message is emitted when inventory is empty
- That the module-level assignment works correctly

**Bug class:** If someone refactored `core/inventory.py` to, say, assign `devices = None` instead of `devices = {}` when NetBox is unavailable, all device lookups would crash with `AttributeError` instead of returning clean errors. No test catches this.

#### S3-003: `ingest.py::ingest()` main function — untested

**Source:** `ingest.py` lines 130-177
**Test file:** `test_ingest.py` covers `extract_metadata()`, `_router_to_markdown()`, `load_network_context()` — but NOT `ingest()` itself

The main `ingest()` function handles: reading docs from `DOCS_DIR`, chunking with `RecursiveCharacterTextSplitter`, embedding via HuggingFace, writing to ChromaDB, and `--clean` flag handling. None of this is tested.

**Bug class:** A bug in the chunking logic (e.g., metadata not propagating to chunks — which actually exists on line 158 where `chunk.metadata = doc.metadata.copy()` overwrites the splitter's metadata) would cause ChromaDB to contain chunks with wrong metadata. RAG filtering would break silently. No test catches this.

#### S3-004: Vault happy-path response parsing — untested

**Source:** `core/vault.py` lines 25-36 (the `try` block in `get_secret`)
**Test file:** `test_vault.py` — tests cache, fallback, sentinel, but **not** a successful Vault API call

No test verifies that `get_secret()` correctly parses a Vault KV v2 response (`response["data"]["data"]`). If the response structure changed (e.g., Vault v3 API), the test suite would not detect it.

**Bug class:** A real Vault response has the shape `{"data": {"data": {"key": "value"}}}`. If someone changed the parsing to `response["data"]` (missing one level), all Vault lookups would return a dict instead of a string. No test catches this.

### MEDIUM Priority

#### S3-005: Transport semaphore behavior — untested

**Source:** `transport/__init__.py` line 11: `_cmd_sem = asyncio.Semaphore(SSH_MAX_CONCURRENT)`
**Test file:** `test_transport.py` — tests success/error paths but not concurrency

No test verifies that the semaphore limits concurrent SSH connections to `SSH_MAX_CONCURRENT`. A bug that removed the `async with _cmd_sem:` line would go undetected.

#### S3-006: MCP tool invocation — untested

**Source:** `server/MCPServer.py` lines 22-24
**Test file:** `test_mcp_server.py` — verifies tool names and count only

No test verifies that calling a registered MCP tool actually invokes the underlying function with correct parameters. The test only checks registration metadata (names, count), not the FastMCP dispatch pipeline.

#### S3-007: VyOS live test coverage — missing

**Source:** `testing/live/test_platform_coverage.py` `TEST_DEVICES` dict (line 15-21)
VyOS (`R6` in `MOCK_DEVICES`, `cli_style: "vyos"`) has no entry in `TEST_DEVICES`. VyOS is fully defined in `PLATFORM_MAP` and has a custom Scrapli definition (`vyos_vyos.yaml`), but is never tested against a real device.

**Note:** This may be intentional if no VyOS device exists in the lab. Should be documented either way.

#### S3-008: `_get_vectorstore()` lazy init and race condition — untested

**Source:** `tools/rag.py` lines 19-30
No test covers:
- First-call initialization of `_embeddings` and `_vectorstore`
- What happens if `_CHROMA_DIR` does not exist
- Thread/task safety of the global mutable state (no lock protects `_vectorstore`)

### LOW Priority

#### S3-009: `ingest.py` `--clean` flag — untested

The `--clean` argument at `ingest.py` line 174 performs `shutil.rmtree(CHROMA_DIR)`. No test verifies this behavior.

#### S3-010: `run_tests.sh` itself — no validation tests

The test runner script has logic for counting passed/failed/skipped that could be incorrect without detection.

---

## 6. Security Test Gaps

### Input Validation (Code-Enforced) — **WELL COVERED**

| Guardrail | Automated Test | Status |
|-----------|---------------|--------|
| VRF regex validation | `test_input_models.py::test_vrf_injection_rejected` | **Covered** — semicolons, pipes, spaces, too-long, empty |
| OSPF query allowlist | `test_input_models.py::test_invalid_query_rejected` | **Covered** |
| KBQuery vendor allowlist | `test_input_models.py::test_invalid_vendor_rejected` | **Covered** |
| KBQuery topic allowlist | `test_input_models.py::test_invalid_topic_rejected` | **Covered** |
| KBQuery max length | `test_input_models.py::test_query_too_long` | **Covered** |
| top_k range enforcement | `test_input_models.py::test_top_k_too_high/too_low` | **Covered** |
| Adversarial device names | `test_tools.py::TestAdversarialDeviceName` | **Covered** — injection payloads, SQL injection, overflow, empty |
| JSON string parsing | `test_input_models.py::test_json_string_parsing/malformed` | **Covered** |

### Security Gaps

#### S3-SEC-001: Error message content leakage — NOT tested

No test verifies that error messages returned by tool functions do not leak internal paths, stack traces, or credentials. For example, `transport/__init__.py` line 26: `return {"device": device_name, "cli_style": device["cli_style"], "error": str(e)}` — the raw exception `str(e)` could contain sensitive information (e.g., connection strings, internal IPs). No test asserts that error messages are sanitized.

**Recommendation:** Add tests that verify error dict values do not contain file paths, credentials, or stack traces. Assert `"password" not in result["error"].lower()` for SSH failure scenarios.

#### S3-SEC-002: `SSH_STRICT_HOST_KEY` parsing — NOT tested

`core/settings.py` line 13: `SSH_STRICT_HOST_KEY = os.getenv("SSH_STRICT_HOST_KEY", "").lower() in ("true", "1", "yes")`. The default when env var is unset is `False` (empty string not in the tuple). This means **host key verification is OFF by default**. Whether this is intentional or a security issue, it is not tested. A refactor that accidentally changed this to `True` by default (or vice versa) would not be caught.

#### S3-SEC-003: Guardrail for no `run_show` tool — NOT automatically tested

The guardrails document states YANA deliberately omits a `run_show` tool. No automated test verifies that the MCP server exposes exactly the allowed set of tools (only `test_mcp_server.py::test_tool_names` does this, which is a positive — it verifies the exact set `{"search_knowledge_base", "get_ospf", "get_interfaces"}`). This IS covered.

#### S3-SEC-004: VRF value reaches command string safely — tested but incomplete

`test_tools.py::TestVrfEndToEnd::test_explicit_vrf_in_final_command` verifies VRF flows into the command. But no test verifies that a VRF value that passes Pydantic validation but contains characters that could be misinterpreted by certain platforms (e.g., `VRF-1` with a dash on a platform that uses dashes as argument separators) is handled safely.

---

## 7. Test Infrastructure Issues

### S4-001: `run_tests.sh` — Failure detection based on string matching (fragile)

**File:** `testing/run_tests.sh`, lines 26-36

The `run_suite()` function determines pass/fail by grepping pytest output for the string `"failed"`:
```bash
if echo "$output" | grep -qE "failed"; then
```

This has two problems:
1. **False positive:** If a test _name_ contains the word "failed" (e.g., `test_vault_failure_sets_sentinel`) and that test is listed in the output summary, the grep could match even on a passing suite.
2. **False negative:** If pytest crashes before running tests (e.g., import error, conftest error), the output may contain `"ERROR"` but not `"failed"`, causing the suite to be reported as `PASS`.

**Fix:** Use pytest's exit code instead of grepping output. Remove `|| true` from line 24 and capture the exit code:
```bash
$PYTHON -m pytest "$path" "${extra_args[@]}" --tb=short -q 2>&1
exit_code=$?
```

### S4-002: `run_tests.sh` — Suite-level granularity masks individual test failures

The script reports one PASS/FAIL per suite. If 9 of 10 tests pass and 1 fails, the entire suite shows FAIL with up to 5 lines of detail. This is acceptable for a summary but could hide the severity of failures.

### S4-003: CI pipeline runs `ingest.py` with `NETBOX_URL=""` — no validation

**File:** `.github/workflows/ci.yml`, lines 37-39

CI runs `python ingest.py` to populate ChromaDB before tests. It sets `NETBOX_URL: ""`, which disables NetBox loading. This means:
- CI always tests with file-based docs only — never with NetBox-derived intent/inventory
- If `ingest.py` errors when `NETBOX_URL` is empty but `NETBOX_TOKEN` is set (from a stale env var), the CI step could fail unexpectedly

This is a **minor** concern — the empty-NETBOX_URL path is tested in `test_netbox.py`.

### S4-004: No pytest timeout in `pytest.ini`

**File:** `pytest.ini` — contains only `asyncio_mode = auto`

The CI workflow passes `--timeout=30` but local runs via `run_tests.sh` or direct `pytest` do not include a timeout. A hanging test (e.g., from an accidental real SSH connection) would block indefinitely locally.

**Fix:** Add `timeout = 30` to `pytest.ini`.

### S4-005: `conftest.py` patches `transport.devices` but not `transport.execute_ssh`

**File:** `testing/automated/conftest.py`

The autouse fixture patches `devices` dicts in four modules but does not patch `execute_ssh`. Individual tests must patch SSH themselves. This is **by design** (tests need different SSH mock behaviors), but means that if any test forgets to patch SSH and uses a device from `MOCK_DEVICES`, it would attempt a real SSH connection to `10.0.0.x` — which would hang or fail depending on network.

---

## 8. Per-Suite Detailed Verdicts

### UT-001: Input Model Validation — EXCELLENT

**Covers:** `input_models/models.py` — `OspfQuery`, `InterfacesQuery`, `KBQuery`, `BaseParamsModel.parse_string_input`, VRF regex validation
**Strengths:** Comprehensive parametrized injection tests (semicolon, pipe, space, overflow, empty). Boundary value tests (max length, top_k limits). JSON string parsing for MCP protocol compatibility. All Pydantic `Literal` enums tested for rejection of invalid values.
**Weaknesses:** No test for `InterfacesQuery` with extra/unexpected fields (Pydantic `model_config` behavior). No test for Unicode in VRF names (e.g., Cyrillic characters that look like ASCII).

### UT-002: Platform Map — EXCELLENT

**Covers:** `platforms/platform_map.py` — `PLATFORM_MAP` structure, `_apply_vrf()`, `get_action()`
**Strengths:** Structural completeness test (all 6 cli_styles present, all 6 OSPF queries per style, interfaces present). VRF substitution tested for dict-with-default/vrf, plain strings, None VRF. `get_action()` tested for VRF override vs. device fallback. Error paths (unknown cli_style, unknown category) tested.
**Weaknesses:** None significant. This is a model test suite.

### UT-003: Tool Layer — SOLID

**Covers:** `tools/__init__.py::_error_response()`, `tools/ospf.py::get_ospf()`, `tools/operational.py::get_interfaces()`
**Strengths:** Tests unknown device error path, multi-vendor cli_style verification (ios, eos, junos), VRF pass-through, VRF override, adversarial device names (injection payloads). The `_command` assertion verifies platform-map resolution, not just mock passthrough.
**Weaknesses:** `test_adversarial_name_returns_clean_error` (line 93-97) has a loose assertion (`assert "error" in result`) without checking the error message content. An adversarial name could trigger an unexpected error type (e.g., from Pydantic validation) and the test would still pass.

### UT-004: Transport Dispatcher — SOLID

**Covers:** `transport/__init__.py::execute_command()`
**Strengths:** Tests unknown device error shape (only `"error"` key), SSH failure error shape (includes `device` and `cli_style`), success return shape. Error message content verified (`"Unknown device"`, `"SSH timeout"`).
**Weaknesses:** Semaphore behavior untested. No test for `timeout_ops` parameter passthrough.

### UT-005: Vault Client — GOOD

**Covers:** `core/vault.py::get_secret()` — env var fallback, cache hit, cache miss on key, sentinel caching
**Strengths:** Tests the full fallback chain: no VAULT_ADDR -> env var; no VAULT_ADDR + no fallback -> None; cache hit; cache miss key -> fallback; Vault failure -> sentinel + fallback.
**Weaknesses:** **No happy-path test.** There is no test that mocks a successful Vault API response and verifies that `get_secret()` correctly parses `response["data"]["data"]` and returns the requested key. This is a significant gap (S3-004). Also, `_cache.clear()` in `setup_method` resets cache state but does not reset the module-level `_VAULT_FAILED` sentinel object — this is fine since `_VAULT_FAILED = object()` is immutable and module-level.

### UT-006: Ingest Helpers — GOOD

**Covers:** `ingest.py::extract_metadata()`, `_router_to_markdown()`, `load_network_context()`
**Strengths:** Tests vendor file detection for all 5 vendors, RFC detection, unknown file defaults. `_router_to_markdown()` tested with full OSPF data, BGP data, and minimal router. `load_network_context()` tested for NetBox intent, JSON fallback, and inventory document metadata.
**Weaknesses:** Main `ingest()` function completely untested (S3-003). `extract_metadata()` for intent/inventory files not tested (only vendor/rfc/general paths).

### UT-007: NetBox Loader — EXCELLENT

**Covers:** `core/netbox.py::load_devices()`, `load_intent()`
**Strengths:** Thorough error path coverage: no URL, no token, pynetbox exception, empty device list, missing primary_ip, missing cli_style, per-device exception resilience. Valid device parsing with exact field verification. `load_intent()` tests both yana- and dblcheck- prefix fallback, global context for autonomous_systems, exception handling.
**Weaknesses:** None significant. The mock shape (`_make_nb_device`) matches the real pynetbox device record structure accurately.

### UT-008: SSH Layer — SOLID

**Covers:** `transport/ssh.py::_build_cli()`, `execute_ssh()`
**Strengths:** MikroTik `+ct` suffix and `\r\n` return char tested. VyOS `Ssh2Options` vs. standard `BinOptions` path tested. Vault credential vs. global credential fallback tested. `execute_ssh()` retry logic: `OpenException` no-retry, generic exception retry+recover, retries exhausted.
**Weaknesses:** `_build_cli` assertion on `mock_cli.call_args.kwargs["auth_options"]` accesses the `AuthOptions` object that was passed to the mock, not the real `Cli` constructor. Since `AuthOptions` is a real Scrapli object (not mocked), the attribute checks are valid. No test for `SSH_STRICT_HOST_KEY` paths (True vs. False affect `BinOptions` construction).

### UT-009: MCP Server Registration — MINIMAL

**Covers:** `server/MCPServer.py` — tool count and names only
**Strengths:** Verifies the exact tool set, preventing accidental addition/removal of tools.
**Weaknesses:** Does not test tool invocation through FastMCP, parameter passing, or error handling. This is registration-only coverage.

### IT-001: RAG Pipeline — CONDITIONAL

**Covers:** `tools/rag.py::search_knowledge_base()` — basic query, metadata shape, vendor/topic/compound filtering, top_k, error path
**Strengths:** Comprehensive filtering tests including the `$and` compound filter (which was a real bug vector per ChromaDB API). Error path test mocks `_get_vectorstore` failure and verifies structured error response. `top_k` limit tested at both custom and default values.
**Weaknesses:** **Conditionally skipped** when ChromaDB is not populated (`pytestmark` skipif). CI populates ChromaDB via `ingest.py`, but local runs often skip this suite. The skip message is clear and appropriate.

### LT-001: Platform Coverage — SOLID

**Covers:** 5 vendors (ios, eos, junos, aos, routeros) x 7 queries (6 OSPF + 1 interfaces) = 35 tests
**Strengths:** Real device validation. `classify()` function detects vendor-specific error patterns (`"% "`, `"error:"`, `"Invalid input"`, `"syntax error"`). Results written to markdown report with timestamps and commands.
**Weaknesses:** VyOS not covered (S3-007). `EMPTY` result is treated as a pass (`assert status != "FAIL"`), meaning a command that returns empty output is not flagged. This is intentional (some OSPF queries return empty on devices with no OSPF config) but could mask real issues.

### MT-001: Manual Tests — GOOD

**Covers:** 10 scenarios: basic query, multi-tool, KB search, vendor filter, design intent, unknown device error, read-only enforcement, no-run_show limitation, cross-device corroboration, out-of-scope topic
**Strengths:** Covers behavioral guardrails (read-only policy, no run_show) that cannot be automated. Cross-device adjacency corroboration tests the agent's reasoning capability.
**Weaknesses:** No structured pass/fail tracking mechanism. Results are self-reported.

---

## 9. Feature-to-Test Traceability Matrix

| Feature | Tested By | Coverage Level |
|---------|-----------|---------------|
| Input validation (OspfQuery) | UT-001 | **Full** |
| Input validation (KBQuery) | UT-001 | **Full** |
| Input validation (InterfacesQuery) | UT-001 | **Minimal** |
| VRF injection prevention | UT-001, UT-003 | **Full** |
| VRF handling (platform-map resolution) | UT-002, UT-003 | **Full** |
| Platform map structure | UT-002 | **Full** |
| Platform map — get_action() | UT-002 | **Full** |
| Transport — execute_command() | UT-004 | **Good** |
| Transport — semaphore concurrency | None | **Not tested** |
| Vault — env var fallback | UT-005 | **Full** |
| Vault — cache behavior | UT-005 | **Full** |
| Vault — sentinel caching | UT-005 | **Good** |
| Vault — happy-path API response | None | **Not tested** |
| NetBox — load_devices() | UT-007 | **Full** |
| NetBox — load_intent() | UT-007 | **Full** |
| Inventory — import-time loading | None | **Not tested** |
| Settings — credential loading | None | **Not tested** |
| Settings — SSH config values | None | **Not tested** |
| SSH — _build_cli() vendor paths | UT-008 | **Good** |
| SSH — execute_ssh() retry logic | UT-008 | **Full** |
| SSH — OpenException no-retry | UT-008 | **Full** |
| SSH — strict host key paths | None | **Not tested** |
| Ingest — extract_metadata() | UT-006 | **Full** |
| Ingest — _router_to_markdown() | UT-006 | **Full** |
| Ingest — load_network_context() | UT-006 | **Good** |
| Ingest — main ingest() pipeline | None | **Not tested** |
| RAG search — basic query | IT-001 (conditional) | **Good** |
| RAG search — filtering | IT-001 (conditional) | **Full** |
| RAG search — error handling | IT-001 (conditional) | **Good** |
| RAG — _get_vectorstore() init | None | **Not tested** |
| MCP — tool registration | UT-009 | **Good** |
| MCP — tool invocation | None | **Not tested** |
| Live multi-vendor coverage | LT-001 | **Good** (5/6 vendors) |
| Live VyOS coverage | None | **Not tested** |
| Security — adversarial inputs | UT-001, UT-003 | **Good** |
| Security — error message sanitization | None | **Not tested** |
| Security — no run_show tool | UT-009 | **Partial** (name check only) |
| Security — read-only enforcement | MT-001 | **Manual only** |

---

## 10. Prioritized Recommendations

### P0 — Fix Before Next Release

#### P0-1: Add Vault happy-path test (S3-004)

The entire credential chain depends on Vault response parsing. Zero test coverage on the happy path means a breaking change to the parsing logic would be undetected.

**Fix:** In `test_vault.py`, add a test that mocks `hvac.Client` to return a properly structured response:
```python
def test_successful_vault_lookup(self, monkeypatch):
    monkeypatch.setenv("VAULT_ADDR", "http://fake:8200")
    monkeypatch.setenv("VAULT_TOKEN", "fake-token")
    import core.vault
    mock_hvac = MagicMock()
    mock_hvac.Client.return_value.secrets.kv.v2.read_secret_version.return_value = {
        "data": {"data": {"username": "admin", "password": "secret"}}
    }
    with patch.dict("sys.modules", {"hvac": mock_hvac}):
        result = core.vault.get_secret("yana/router", "password")
    assert result == "secret"
    assert core.vault._cache["yana/router"] == {"username": "admin", "password": "secret"}
```

#### P0-2: Add `core/settings.py` test (S3-001)

**Fix:** Create `testing/automated/test_settings.py`:
```python
def test_ssh_strict_host_key_parsing(monkeypatch):
    monkeypatch.setenv("SSH_STRICT_HOST_KEY", "true")
    # Re-evaluate the expression
    result = monkeypatch.getenv("SSH_STRICT_HOST_KEY", "").lower() in ("true", "1", "yes")
    assert result is True

def test_ssh_strict_host_key_default_is_false(monkeypatch):
    monkeypatch.delenv("SSH_STRICT_HOST_KEY", raising=False)
    result = os.getenv("SSH_STRICT_HOST_KEY", "").lower() in ("true", "1", "yes")
    assert result is False
```
Note: Since `core/settings.py` evaluates at import time, testing requires careful re-import or refactoring the settings to be function-based.

#### P0-3: Fix `run_tests.sh` failure detection (S4-001)

**Fix:** Replace string-matching with exit code checking in `run_suite()`:
```bash
run_suite() {
    local id="$1"
    local name="$2"
    local path="$3"
    shift 3
    local extra_args=("$@")

    printf "%s[%s] %s%s ... " "$BOLD" "$id" "$name" "$NC"
    output=$($PYTHON -m pytest "$path" "${extra_args[@]}" --tb=short -q 2>&1)
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        printf "%sPASS%s\n" "$GREEN" "$NC"
        PASSED=$((PASSED + 1))
    elif [ $exit_code -eq 5 ]; then
        printf "%sSKIP%s\n" "$YELLOW" "$NC"
        SKIPPED=$((SKIPPED + 1))
    else
        printf "%sFAIL%s\n" "$RED" "$NC"
        echo "$output" | tail -10
        FAILED=$((FAILED + 1))
    fi
}
```
(Pytest exit code 5 = no tests collected/all skipped)

### P1 — Address in Next Sprint

#### P1-1: Add `core/inventory.py` import-time behavior test (S3-002)

Test that when `load_devices()` returns `None`, `devices` is an empty dict (not `None`), and when it returns a dict, `devices` contains the expected entries.

#### P1-2: Add SSH `strict_host_key` path test (S3 subset of S3-001)

In `test_ssh.py`, add tests for `_build_cli` with `SSH_STRICT_HOST_KEY=True` verifying `BinOptions(enable_strict_key=True, known_hosts_path=...)` is called.

#### P1-3: Add transport semaphore test (S3-005)

Test that `execute_command` uses the semaphore by verifying concurrent calls are limited.

#### P1-4: Add error message sanitization tests (S3-SEC-001)

In `test_transport.py` and `test_tools.py`, assert that error dicts from SSH failures do not contain sensitive patterns (file paths, credentials, internal IPs).

#### P1-5: Strengthen adversarial device name assertions (UT-003 weakness)

In `test_tools.py::TestAdversarialDeviceName::test_adversarial_name_returns_clean_error`, add:
```python
assert "Unknown device" in result["error"]
```
This ensures the error is from the inventory lookup, not an unexpected exception.

#### P1-6: Add `pytest.ini` timeout (S4-004)

Add `timeout = 30` to `pytest.ini` to prevent hanging tests in local runs.

### P2 — Backlog

#### P2-1: Add MCP tool invocation test (S3-006)

Test that calling `mcp.call_tool("get_ospf", ...)` invokes `get_ospf()` with the correct parameter model.

#### P2-2: Add `ingest()` pipeline test (S3-003)

Mock ChromaDB and verify that `ingest()` reads docs, chunks them, and calls `Chroma.from_documents()` with correct arguments.

#### P2-3: Document VyOS live test gap (S3-007)

Either add a VyOS device to the lab and `TEST_DEVICES`, or add a comment/skip marker explaining why VyOS is excluded from live tests.

#### P2-4: Add `_get_vectorstore()` initialization test (S3-008)

Test that `_get_vectorstore()` initializes embeddings and vectorstore on first call, and returns the cached instance on subsequent calls.

#### P2-5: Test `InterfacesQuery` with unexpected fields

Add a test verifying that `InterfacesQuery(device="R1", extra_field="bad")` either rejects or ignores the extra field, depending on Pydantic `model_config`.

#### P2-6: Add Unicode VRF test

Test that Unicode characters in VRF names (e.g., Cyrillic `а` that looks like Latin `a`) are rejected by the regex validator.
