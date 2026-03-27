# netKB Test Quality Audit Report

**Date:** 2026-03-27
**Auditor:** External QA (automated analysis)
**Scope:** All test suites under `testing/`, CI pipeline, source modules for mock fidelity assessment

---

## 1. Executive Summary

The netKB test suite is **structurally sound** — it covers the critical boundaries (input validation, platform map resolution, VRF injection, credential chain, NetBox parsing) with specific assertions that would genuinely fail under mutation. The most critical finding is in **IT-001 (RAG Pipeline)**, where `test_basic_query` uses `len(result["results"]) > 0`, a trivially-true assertion that cannot distinguish correct retrieval from garbage results. The dominant theme across the suite is **conditional coverage**: the RAG integration tests skip entirely without ChromaDB, and there is no CI-level guarantee they have ever been exercised in the pipeline (they have, due to the `ingest.py` step in CI), while several source modules (`core/settings.py`, `core/inventory.py`, the main `ingest()` function) have zero direct test coverage.

---

## 2. Verdict Summary Table

| Suite ID | Suite Name | Test Count | Verdict |
|----------|-----------|------------|---------|
| UT-001 | Input Model Validation | 14 | **EXCELLENT** |
| UT-002 | Platform Map | 13 | **EXCELLENT** |
| UT-003 | Tool Layer | 11 | **SOLID** |
| UT-004 | Transport Dispatcher | 5 | **SOLID** |
| UT-005 | Vault Client | 5 | **SOLID** |
| UT-006 | Ingest Helpers | 9 | **GOOD** |
| UT-007 | NetBox Loader | 12 | **EXCELLENT** |
| UT-008 | SSH Layer | 8 | **EXCELLENT** |
| UT-009 | MCP Server Registration | 2 | **MINIMAL** |
| IT-001 | RAG Pipeline | 7 | **CONDITIONAL** |
| LT-001 | Platform Coverage | 35 (parametrized) | **GOOD** |
| MT-001 | Manual Tests | 10 | **GOOD** |

---

## 3. Ghost Conditions and Silent Passes (S1)

### Finding S1-1: `test_basic_query` uses trivially-satisfiable assertion

**File:** `testing/automated/test_rag_pipeline.py:33`
**Assertion:** `assert len(result["results"]) > 0`
**Why it is a ghost:** This assertion passes as long as ChromaDB returns *any* document for *any* query. It does not verify that the results are relevant to "OSPF neighbor states." If the embedding model were replaced with a random vector generator, or if the ChromaDB contained only unrelated documents, this test would still pass. The assertion tests ChromaDB liveness, not retrieval correctness.
**Severity:** S1
**Fix:** Assert that at least one result's `content` contains a query-relevant substring (e.g., `assert any("neighbor" in r["content"].lower() or "adjacency" in r["content"].lower() for r in result["results"])`). This is still a coarse check but distinguishes correct retrieval from garbage.

### Finding S1-2: `test_adversarial_name_returns_clean_error` has no assertion on error content

**File:** `testing/automated/test_tools.py:96-97`
**Assertion:** `assert "error" in result` (line 96), then a comment "No exception raised, no command executed" with no further assertion.
**Why it is a ghost:** The assertion `"error" in result` is satisfied by *any* error, including an unrelated internal error (e.g., `TypeError`, `KeyError` caught by a blanket `except`). It does not verify that the error message says "Unknown device" or that it references the adversarial input. If `get_ospf` raised an unhandled exception for adversarial inputs and a surrounding `try/except` caught it generically, this test would still pass.
**Severity:** S1
**Fix:** Assert the error message content: `assert "Unknown device" in result["error"]` or `assert bad_device in result["error"]`. The existing `test_unknown_device` tests in the same file already demonstrate this pattern.

### Finding S1-3: `test_valid_device_ios` in `TestGetInterfaces` has a weak `raw` presence check

**File:** `testing/automated/test_tools.py:65`
**Assertion:** `assert "raw" in result`
**Why it is a ghost (partial):** This assertion only checks that the key `"raw"` exists in the result dict. It does not verify the content. The transport layer always adds `"raw"` to the result dict when `execute_ssh` succeeds (per `transport/__init__.py:28-33`), so this is effectively testing dict construction, not tool behavior. However, the same test also asserts `result["device"] == "R1"` and `result["cli_style"] == "ios"`, which are real assertions. The `"raw" in result` assertion is individually a ghost but the test as a whole is not.
**Severity:** S1 (for this specific assertion line only; test overall is S4)
**Fix:** Replace `assert "raw" in result` with `assert "GigabitEthernet0/0" in result["raw"]` or at minimum `assert result["raw"]` (verifies non-empty).

---

## 4. Mock Fidelity Analysis (S2)

### Finding S2-1: `_make_nb_device` mock `custom_fields` is a plain dict; real pynetbox returns a pynetbox `Record`

**File:** `testing/automated/test_netbox.py:18`
**Mock:** `dev.custom_fields = {"cli_style": cli_style, "vrf": vrf}`
**Real:** In pynetbox, `custom_fields` is a dict (or sometimes a `Record` depending on version), but in practice `.get()` works the same way.
**Impact:** LOW. The real code uses `(dev.custom_fields or {}).get("cli_style", "")` which handles both dict and Record. This mock faithfully produces the same `.get()` behavior. **No structural mismatch.**
**Verdict:** No action needed.

### Finding S2-2: `_async_cm` does not replicate Scrapli's `Cli` connection lifecycle faithfully

**File:** `testing/automated/test_ssh.py:14-21`
**Mock:** Returns a `MagicMock()` with `send_input_async` returning a `MagicMock(result=raw_result)`.
**Real:** `Cli.__aenter__` returns a `Cli` instance (not a separate connection object); `send_input_async` returns a Scrapli `Response` object with `.result` attribute.
**Impact:** MEDIUM. The test correctly verifies that `execute_ssh` extracts `.result` from the response. However, `_async_cm` returns a `mock_conn` from `__aenter__` that is a separate object from the `Cli` mock itself. In real Scrapli, `async with Cli(...) as conn:` returns the same `Cli` instance. This structural difference is benign because the test only accesses `conn.send_input_async`, which works the same way on both the mock and the real object.
**Verdict:** No action needed, but documenting this mock structure would help future maintainers.

### Finding S2-3: `test_vault_failure_sets_sentinel` patches `hvac` via `sys.modules` but does not match real `hvac.Client` construction

**File:** `testing/automated/test_vault.py:62-64`
**Mock:** `hvac.Client.return_value.secrets.kv.v2.read_secret_version.side_effect = Exception("unreachable")`
**Real:** `vault.py` does `client = hvac.Client(url=..., token=...)` then `client.session.timeout = (5, 10)` then `client.secrets.kv.v2.read_secret_version(...)`.
**Impact:** LOW. `MagicMock()` auto-creates attributes, so `client.session.timeout = (5, 10)` succeeds silently on the mock. The mock chain `Client.return_value.secrets.kv.v2.read_secret_version.side_effect` correctly targets the same call chain the real code uses. The mock is functionally faithful.
**Verdict:** No action needed.

### Finding S2-4: Transport `execute_ssh` mock returns a `str`, matching real signature

**File:** `testing/automated/test_tools.py:31-32` and `testing/automated/test_transport.py:13-14`
**Mock:** `mock_ssh.return_value = "Neighbor ID  State\n1.1.1.1  FULL"`
**Real:** `execute_ssh()` returns `str` (the `.result` attribute of a Scrapli Response).
**Verdict:** Faithful. No issue.

**Overall mock fidelity assessment:** No S2 issues that would cause a test to pass when real code fails. The mocks accurately represent the contracts of the dependencies.

---

## 5. Coverage Gap Inventory (S3)

### HIGH Priority

**S3-1: `core/settings.py` has zero test coverage**
- `settings.py` runs Vault calls at import time to resolve `USERNAME` and `PASSWORD`.
- If `get_secret` raises an exception during import (e.g., `hvac` import failure combined with missing env vars), the entire server fails to start.
- If `SSH_RETRIES` were misconfigured to `-1`, the retry loop in `execute_ssh` would iterate `range(0)` (zero iterations), set `last_exc = None`, then `raise None` -> `TypeError`.
- **Bug class:** Configuration-level failures that crash the server at startup.

**S3-2: `core/inventory.py` import-time side effect has no test**
- `inventory.py` calls `load_devices()` at module import time. If NetBox is unreachable, `devices` is set to `{}`.
- No test verifies the behavior of the server when `devices` is empty (all tool calls return "Unknown device" errors silently).
- The conftest `mock_inventory` fixture patches over this, so the import-time behavior is never exercised.
- **Bug class:** Silent total failure — server appears healthy but every device query fails.

**S3-3: `ingest.py::ingest()` main function is not tested**
- The entry point that reads docs, chunks them, embeds them, and writes to ChromaDB has no automated test.
- If chunking logic breaks (e.g., metadata is not preserved through `split_documents`), the entire KB becomes unusable.
- CI runs `python ingest.py` as a setup step, which is an implicit integration test, but failures there would manifest as a CI step failure, not a test failure with diagnostic output.
- **Bug class:** Silent KB corruption — ingest succeeds but metadata is lost, making filtered queries return nothing.

**S3-4: `transport/__init__.py` semaphore behavior under concurrent load is not tested**
- `_cmd_sem = asyncio.Semaphore(SSH_MAX_CONCURRENT)` limits concurrent SSH sessions to 5.
- No test verifies that the 6th concurrent request blocks, or that semaphore release happens correctly on exception.
- **Bug class:** Resource exhaustion or deadlock under concurrent load.

### MEDIUM Priority

**S3-5: `tools/rag.py::_get_vectorstore()` lazy init is not directly tested**
- The lazy singleton pattern (global `_vectorstore` initialized on first call) is exercised indirectly by IT-001, but there is no test for the race condition where two concurrent calls could initialize two vectorstores.
- **Bug class:** Double initialization or thread-safety issue.

**S3-6: VyOS has no live test coverage**
- `TEST_DEVICES` in `test_platform_coverage.py` lists 5 vendors. VyOS is in `PLATFORM_MAP` and `MOCK_DEVICES` but absent from live tests.
- If VyOS command syntax in `PLATFORM_MAP` is wrong, it will only be caught in production.
- **Bug class:** Vendor-specific command failures on VyOS devices.

**S3-7: `get_action()` with unknown `query` (not category) is not tested**
- `test_unknown_category_raises` tests `get_action(device, "bgp", "neighbors")` (unknown category).
- But there is no test for `get_action(device, "ospf", "nonexistent_query")` (valid category, unknown query).
- The real code does `map_entry[category][query]` which would raise `KeyError` for an unknown query, but this path is untested.
- **Bug class:** Unhandled `KeyError` for invalid query within a valid category.

**S3-8: `get_action()` with `KeyError` in `get_ospf` / `get_interfaces` is not tested end-to-end**
- `tools/ospf.py:26-27` catches `KeyError` from `get_action()` and returns an error dict. No test exercises this path.
- **Bug class:** The `KeyError` catch could be removed or broken without any test noticing.

### LOW Priority

**S3-9: MCP server tool invocation is not tested**
- UT-009 verifies tool *registration* (count and names) but not *invocation* through the FastMCP protocol.
- **Bug class:** Tool registered but invocation fails due to parameter serialization mismatch.

**S3-10: `BaseParamsModel.parse_string_input` error path for non-JSON non-dict input is partially tested**
- `test_malformed_json_rejected` tests `"not json at all"` which hits the `JSONDecodeError` path.
- But there is no test for other `model_validator` edge cases (e.g., passing `None`, passing an integer, passing a list).
- **Bug class:** Unexpected input types causing unhelpful error messages.

---

## 6. Security Test Gaps

### Automated security coverage assessment:

| Security Guardrail | Automated Test | Status |
|---|---|---|
| VRF injection (`;`, `\|`, spaces) | `test_vrf_injection_rejected` (UT-001) | **Covered** |
| OSPF query allowlist (Literal enum) | `test_invalid_query_rejected` (UT-001) | **Covered** |
| Vendor enum allowlist | `test_invalid_vendor_rejected` (UT-001) | **Covered** |
| Topic enum allowlist | `test_invalid_topic_rejected` (UT-001) | **Covered** |
| `top_k` boundary (1-10) | `test_top_k_too_high`, `test_top_k_too_low` (UT-001) | **Covered** |
| Query max length (500) | `test_query_too_long`, `test_query_at_max_length` (UT-001) | **Covered** |
| Adversarial device names | `test_adversarial_name_returns_clean_error` (UT-003) | **Partially covered** (S1-2) |
| Static command map (no `run_show`) | Structural — no code path exists | **Covered by design** |
| SSH strict host key | Not tested | **GAP** |
| Error message content leakage | Not tested | **GAP** |
| Vault credential caching | `test_cache_hit`, `test_vault_failure_sets_sentinel` (UT-005) | **Covered** |
| No config-context injection from `CLAUDE.md` deny rules | Not testable in automated tests | **Manual only** |

### Specific security gaps:

**SEC-1: Error messages are not tested for internal information leakage**
- When `execute_ssh` raises `ConnectionError("SSH timeout")`, the error string is passed directly to the client via `str(e)` in `transport/__init__.py:26`.
- No test verifies that error messages do not leak internal IPs, credentials, or stack traces.
- **Risk:** An SSH error containing a traceback or credential path could be exposed to the MCP client (and thus to the LLM and the user).

**SEC-2: `SSH_STRICT_HOST_KEY` enforcement is not tested**
- `core/settings.py` reads `SSH_STRICT_HOST_KEY` from env. `transport/ssh.py` uses it to set `enable_strict_key` on `BinOptions`.
- No test verifies that `SSH_STRICT_HOST_KEY=true` results in `enable_strict_key=True` being passed to `BinOptions`.
- **Risk:** A regression could silently disable host key verification.

**SEC-3: VRF regex boundary values are not fully covered**
- The regex `^[a-zA-Z0-9_-]{1,32}$` is tested with injection payloads, spaces, and length.
- Missing: Unicode characters (e.g., `"VRF\u200b1"` — zero-width space), null bytes (`"VRF\x001"`).
- **Risk:** Low — Pydantic's string validation likely handles these, but explicit tests would confirm.

---

## 7. Test Infrastructure Issues

### INFRA-1: `run_tests.sh` failure detection is grep-based and fragile

**File:** `testing/run_tests.sh:26`
**Issue:** The `run_suite` function detects pass/fail by grepping pytest output for the string "failed". If pytest's output format changes (e.g., a future version uses "FAILED" differently, or a test name contains the word "failed"), the detection logic could misclassify results. The `|| true` on line 24 suppresses pytest's exit code entirely.
**Impact:** A suite could fail silently if the grep pattern does not match.
**Fix:** Use pytest's exit code directly instead of parsing output: `$PYTHON -m pytest "$path" ...; ec=$?; if [ $ec -ne 0 ] && [ $ec -ne 5 ]; then FAILED=...; fi`

### INFRA-2: `pytest.ini` is minimal — no timeout configured

**File:** `pytest.ini`
**Issue:** Only `asyncio_mode = auto` is set. No `timeout` default, no `markers` declared, no `testpaths` configured. CI adds `--timeout=30` but local runs have no timeout, meaning a hanging SSH mock could block indefinitely.
**Fix:** Add `timeout = 30` and `testpaths = testing/automated` to `pytest.ini`.

### INFRA-3: CI does not run `run_tests.sh` — divergence between local and CI execution

**File:** `.github/workflows/ci.yml:41`
**Issue:** CI runs `python -m pytest testing/automated/ -v --tb=short --timeout=30` directly. The local runner `run_tests.sh` runs suites individually with `-q`. The two execution paths could diverge (e.g., `conftest.py` fixture scope behaves differently when running all tests in one pytest invocation vs. individually).
**Impact:** Low, but it means `run_tests.sh` is not validated by CI.
**Fix:** Either have CI call `run_tests.sh` or document that `run_tests.sh` is for local convenience only.

### INFRA-4: No conftest fixture for Vault cache cleanup at the module level

**File:** `testing/automated/test_vault.py:8-10`
**Issue:** `test_vault.py` uses `setup_method` to clear `_cache` before each test. This is correct but fragile — if another test module imports `core.vault` and populates the cache, cross-module pollution is possible. The `conftest.py` does not have a Vault cache cleanup fixture.
**Fix:** Add an autouse fixture to `conftest.py` that clears `core.vault._cache` before each test.

### INFRA-5: IT-001 skip condition means CI must run `ingest.py` first

**File:** `testing/automated/test_rag_pipeline.py:8-11`
**Issue:** The `pytestmark = pytest.mark.skipif(not CHROMA_DIR.exists(), ...)` will silently skip all RAG tests if `ingest.py` was not run. CI handles this correctly (line 37-39 of `ci.yml`), but a developer running `pytest testing/automated/` locally without ingesting first will get 7 silently skipped tests with no warning beyond "skipped."
**Fix:** This is acceptable behavior, but the skip reason message is clear. No change needed, but consider a `conftest.py` warning.

---

## 8. Per-Suite Detailed Verdicts

### UT-001: Input Model Validation — EXCELLENT

**What it covers:** All three input models (`OspfQuery`, `InterfacesQuery`, `KBQuery`), including VRF regex validation, Literal enum enforcement, boundary values (`top_k` 0/11, query length 500/501), JSON string parsing, and malformed input rejection.
**Strengths:** Parametrized VRF injection tests cover 5 adversarial patterns. Boundary values tested at the exact edge. Both valid and invalid paths covered for every model field.
**Weaknesses:** No test for `InterfacesQuery` with a missing `device` field (would raise `ValidationError`). No test for passing `None`, `int`, or `list` to `model_validate()`.

### UT-002: Platform Map — EXCELLENT

**What it covers:** `PLATFORM_MAP` structure (all 6 CLI styles, all 6 OSPF queries, interfaces key), `_apply_vrf()` with dict/string/None combinations, `get_action()` resolution including VRF fallback from device dict and explicit VRF override.
**Strengths:** Tests verify exact command strings (e.g., `"show ip ospf neighbor vrf VRF1"`), not just presence. Error paths (unknown cli_style, unknown category) tested with specific exception types.
**Weaknesses:** No test for unknown query within a valid category (S3-7).

### UT-003: Tool Layer — SOLID

**What it covers:** `_error_response()` shape, `get_ospf()` and `get_interfaces()` for unknown devices, valid devices across multiple vendors (IOS, EOS, JunOS), VRF pass-through end-to-end, adversarial device names.
**Strengths:** The cli_style assertions (`result["cli_style"] == "ios"`) verify that the tool reads from the device dict rather than hardcoding — this is a real behavioral test. The VRF end-to-end test traces the VRF value from input model through `get_action()` into the final `_command` string.
**Weaknesses:** S1-2 (adversarial test has no content assertion). No test for `get_ospf` when `get_action` raises `KeyError` (S3-8). `assert "raw" in result` is a weak assertion (S1-3).

### UT-004: Transport Dispatcher — SOLID

**What it covers:** `execute_command()` for unknown device, successful execution, error shapes (unknown device vs. SSH failure), error content (`"SSH timeout" in result["error"]`).
**Strengths:** Error shape tests verify exact key sets (`set(result.keys()) == {"error"}`), ensuring the error dict structure is correct for both error paths.
**Weaknesses:** No concurrent-load test for the semaphore (S3-4). No test for `timeout_ops` parameter pass-through.

### UT-005: Vault Client — SOLID

**What it covers:** No-Vault fallback (env var and None), cache hit, cache miss on key (fallback), Vault failure sentinel caching.
**Strengths:** Tests the complete credential resolution chain: Vault -> cache -> env var -> None. The sentinel test verifies that `_cache[path] is _VAULT_FAILED` using identity comparison.
**Weaknesses:** No test for successful Vault read (the happy path where Vault actually returns data that gets cached). The `hvac` mock in `test_vault_failure_sets_sentinel` is complex but correct.

### UT-006: Ingest Helpers — GOOD

**What it covers:** `extract_metadata()` for vendor files, RFC files, unknown files, all 5 vendor prefixes. `_router_to_markdown()` for basic, BGP, and minimal routers. `load_network_context()` for NetBox intent, legacy JSON fallback, and inventory document.
**Strengths:** The `_router_to_markdown()` tests verify specific content strings ("Area 0 normal", "Area 1 stub", BGP AS number), ensuring the formatting logic is correct.
**Weaknesses:** Main `ingest()` function is not tested (S3-3). No test for `extract_metadata` with edge-case filenames (e.g., `"vendor_.md"`, `"rfc.md"`).

### UT-007: NetBox Loader — EXCELLENT

**What it covers:** `load_devices()` for: no URL, no token, pynetbox exception, empty device list, valid device parsing, VRF inclusion, missing primary_ip skip, missing cli_style skip, per-device exception resilience. `load_intent()` for: no URL, no contexts, netkb prefix parsing, dblcheck fallback, global context with autonomous_systems, pynetbox exception.
**Strengths:** 12 tests covering virtually every code path. The `_make_nb_device` helper produces realistic mock shapes. The per-device exception test verifies that one broken device does not abort loading of valid devices.
**Weaknesses:** No test for `load_devices()` when `custom_fields` is `None` (the code handles this with `(dev.custom_fields or {})`, but no test exercises this path).

### UT-008: SSH Layer — EXCELLENT

**What it covers:** `_build_cli()` for MikroTik `+ct` suffix, MikroTik `\r\n` return char, standard device BinOptions, VyOS Ssh2Options, Vault password precedence, global credential fallback. `execute_ssh()` for success, OpenException immediate raise (no retry), transient failure recovery on retry, all retries exhausted.
**Strengths:** The retry tests use counting and state variables to verify exact attempt counts. The OpenException test specifically verifies `build_call_count == 1` (no retry). The credential chain tests verify both `auth.username` and `auth.password` on the constructed `Cli` object.
**Weaknesses:** No test for `SSH_TIMEOUT_OPS` pass-through to `SessionOptions`. No test for `SSH_STRICT_HOST_KEY` enforcement (SEC-2).

### UT-009: MCP Server Registration — MINIMAL

**What it covers:** Tool count (exactly 3) and tool names (`search_knowledge_base`, `get_ospf`, `get_interfaces`).
**Strengths:** Correctly verifies the public API surface of the MCP server.
**Weaknesses:** Does not test tool invocation, parameter schema exposure, or error handling through the FastMCP protocol (S3-9). Only 2 tests.

### IT-001: RAG Pipeline — CONDITIONAL

**What it covers:** Basic query returns results, result metadata structure, vendor filter, topic filter, compound filter, intent topic, vectorstore failure error path, top_k limits.
**Strengths:** Filter tests verify that *every* returned result matches the filter criteria (not just the first). The error path test patches `_get_vectorstore` to simulate ChromaDB failure and verifies the structured error response.
**Weaknesses:** S1-1 (basic query uses `len > 0`). All tests are conditionally skipped without ChromaDB. The compound filter test relies on ChromaDB containing documents that match both `vendor="cisco_ios"` and `topic="vendor_guide"` — if the ingested data changes, the test could break or silently return 0 results (though `len > 0` assertion would catch that).

### LT-001: Platform Coverage — GOOD

**What it covers:** All 6 OSPF queries and interface status for 5 vendors (IOS, EOS, JunOS, AOS-CX, RouterOS). Generates a markdown report with pass/empty/fail classification.
**Strengths:** Comprehensive parametrized coverage. The `classify()` function detects vendor-specific error patterns (IOS `%`, AOS `error:`, JunOS `Invalid input`).
**Weaknesses:** VyOS not covered (S3-6). "EMPTY" results are classified as passing (not `FAIL`), which could mask a legitimate issue (device returns blank output for a valid command). No assertion on result content — only that it's not an error.

### MT-001: Manual Tests — GOOD

**What it covers:** 10 scenarios covering basic queries, multi-tool usage, KB search with citations, vendor filtering, design intent, error handling, read-only policy, tool limitation awareness, cross-device corroboration, and out-of-scope topics.
**Strengths:** Well-designed scenarios that test the full agent behavior (LLM + tools + KB), which cannot be automated.
**Weaknesses:** No systematic execution tracking (pass/fail results are not stored). No scenario for VRF-specific queries or concurrent queries.

---

## 9. Feature-to-Test Traceability Matrix

| Feature | Tested By | Coverage Level |
|---------|-----------|---------------|
| OSPF query input validation (Literal enum, VRF regex) | UT-001 | **Full** |
| Interfaces query input validation | UT-001 | **Partial** (no missing-field test) |
| KB query input validation (vendor, topic, top_k, max_length) | UT-001 | **Full** |
| JSON string parsing (`BaseParamsModel`) | UT-001 | **Good** (malformed JSON tested, but not non-string types) |
| VRF handling (injection prevention, substitution, override, fallback) | UT-001, UT-002, UT-003 | **Full** |
| Platform map structure (all vendors, all queries) | UT-002 | **Full** |
| Platform map VRF resolution (`_apply_vrf`, `get_action`) | UT-002 | **Full** |
| Transport dispatcher (`execute_command`) | UT-004 | **Good** |
| Transport semaphore concurrency control | None | **Not tested** |
| Vault credential chain (Vault -> cache -> env -> None) | UT-005 | **Good** (no happy-path Vault read test) |
| Vault failure sentinel caching | UT-005 | **Full** |
| NetBox device loading (all error paths + success) | UT-007 | **Full** |
| NetBox intent loading (prefix fallback, global context) | UT-007 | **Full** |
| SSH connection construction (`_build_cli`) | UT-008 | **Full** |
| SSH retry logic (retry, no-retry on OpenException, exhaustion) | UT-008 | **Full** |
| Ingest metadata extraction | UT-006 | **Full** |
| Ingest markdown conversion | UT-006 | **Good** |
| Ingest network context loading | UT-006 | **Good** |
| Ingest main pipeline (chunk + embed + store) | None (CI implicit) | **Minimal** |
| RAG search (basic, filtered, error path) | IT-001 | **Conditional** |
| MCP tool registration | UT-009 | **Full** (for registration only) |
| MCP tool invocation | None | **Not tested** |
| Live multi-vendor OSPF coverage | LT-001 | **Good** (5/6 vendors) |
| Live VyOS coverage | None | **Not tested** |
| Security: VRF injection prevention | UT-001 | **Full** |
| Security: Adversarial device names | UT-003 | **Partial** (S1-2) |
| Security: Static command map (no run_show) | By design | **Full** |
| Security: SSH strict host key | None | **Not tested** |
| Security: Error message leakage | None | **Not tested** |
| Agent behavior: read-only policy, KB citations, tool selection | MT-001 | **Manual only** |
| `core/settings.py` configuration loading | None | **Not tested** |
| `core/inventory.py` import-time behavior | None | **Not tested** |

---

## 10. Prioritized Recommendations

### P0 — Fix before next release

**P0-1: Fix S1-2 — Add content assertion to `test_adversarial_name_returns_clean_error`**
File: `testing/automated/test_tools.py:96`
Change: `assert "error" in result` -> `assert "Unknown device" in result["error"]`
Rationale: This test is a security-relevant assertion. Without verifying the error message, it cannot distinguish between the intended "Unknown device" response and an accidental internal error. External reviewers will flag this.

**P0-2: Fix S1-1 — Strengthen `test_basic_query` assertion in RAG pipeline**
File: `testing/automated/test_rag_pipeline.py:33-34`
Change: Add `assert any("neighbor" in r["content"].lower() or "state" in r["content"].lower() or "adjacency" in r["content"].lower() for r in result["results"])` after the `len > 0` check.
Rationale: The current assertion is indistinguishable from a liveness check. The IT-001 suite is the only automated validation of the entire RAG pipeline, so its assertions must test retrieval quality, not just database connectivity.

### P1 — Address in next sprint

**P1-1: Add `core/settings.py` unit tests (S3-1)**
Create `testing/automated/test_settings.py` with tests for: (1) `USERNAME`/`PASSWORD` resolve from env vars when Vault is unavailable, (2) `SSH_STRICT_HOST_KEY` parses `"true"`, `"1"`, `"yes"`, `""`, `"false"` correctly, (3) All constants have expected default values.

**P1-2: Add `core/inventory.py` import-time behavior test (S3-2)**
Test that when `load_devices()` returns `None`, `devices` is `{}`. Test that when `load_devices()` returns a valid dict, `devices` is populated. This requires careful import isolation (use `importlib.reload`).

**P1-3: Fix `run_tests.sh` failure detection (INFRA-1)**
Replace the grep-based pass/fail detection with pytest exit code checking: capture `$?` after pytest and classify based on exit codes (0=pass, 1=fail, 5=no tests collected).

**P1-4: Add SSH strict host key enforcement test (SEC-2)**
In `test_ssh.py`, add a test that patches `SSH_STRICT_HOST_KEY` to `True` and verifies that `BinOptions` is called with `enable_strict_key=True` and a valid `known_hosts_path`.

**P1-5: Add unknown-query-within-valid-category test (S3-7)**
In `test_platform_map.py::TestGetAction`, add:
```python
def test_unknown_query_raises(self):
    device = {"cli_style": "ios"}
    with pytest.raises(KeyError):
        get_action(device, "ospf", "nonexistent_query")
```

**P1-6: Fix S1-3 — Strengthen `assert "raw" in result`**
File: `testing/automated/test_tools.py:65`
Change to: `assert result["raw"]` (at minimum, asserts non-empty) or better: `assert "GigabitEthernet" in result["raw"]`.

### P2 — Backlog

**P2-1: Add semaphore concurrency test (S3-4)**
Create an async test that launches `SSH_MAX_CONCURRENT + 1` concurrent `execute_command` calls with a slow mock, verifies that exactly `SSH_MAX_CONCURRENT` run simultaneously, and the extra one blocks until a slot opens.

**P2-2: Add MCP tool invocation test (S3-9)**
Test that calling `mcp.call_tool("get_ospf", {...})` returns the expected result shape (requires mocking transport but exercising the full FastMCP dispatch path).

**P2-3: Add `ingest()` main function test (S3-3)**
Create an integration test that ingests a small set of test documents into a temporary ChromaDB directory, then queries it to verify metadata preservation through the chunk/embed/store pipeline.

**P2-4: Add VyOS to live test coverage (S3-6)**
If a VyOS device is available in the lab, add `"F1V": "vyos"` (or appropriate hostname) to `TEST_DEVICES` in `test_platform_coverage.py`.

**P2-5: Add error message leakage test (SEC-1)**
In `test_transport.py`, add a test that simulates an SSH error with a verbose exception message containing an IP address, and verify that the error dict's `"error"` value does not contain credential-adjacent strings.

**P2-6: Add `pytest.ini` timeout and testpaths configuration (INFRA-2)**
Add `timeout = 30` and `testpaths = testing/automated` to `pytest.ini` for local development parity with CI.

**P2-7: Add Vault happy-path test**
Add a test to `test_vault.py` that mocks a successful Vault read (hvac returns data) and verifies: (1) the returned value matches the Vault data, (2) the path is cached, (3) subsequent calls use the cache.

---

## Appendix: Tests Verified as Non-Ghost

The following tests were evaluated against the ghost-pass checklist and confirmed to be genuine:

- **UT-001 all tests:** Assertions are against Pydantic-constructed model attributes, not mocks. Invalid inputs raise `ValidationError` which is specific enough.
- **UT-002 `test_resolves_ios_ospf_neighbors`:** Asserts exact command string `"show ip ospf neighbor"` — this is the real output of `get_action()`, not a mock value.
- **UT-003 `test_valid_device_ios` (get_ospf):** The `cli_style` assertion verifies that `get_ospf` reads from `MOCK_DEVICES["R1"]` (which has `"cli_style": "ios"`) rather than from the mock SSH return value. The `_command` assertion verifies that `get_action()` resolved the correct command. These are real behavioral tests.
- **UT-005 `test_vault_failure_sets_sentinel`:** The `assert core.vault._cache["fail/path"] is core.vault._VAULT_FAILED` uses identity comparison against the sentinel object, which is a precise assertion.
- **UT-007 `test_valid_device_parsed_correctly`:** Asserts `result["R1"]["host"] == "10.0.0.1"` which requires that `load_devices()` correctly parsed the mock pynetbox device's `primary_ip.address` by splitting on "/" and extracting the IP.
- **UT-008 `test_open_exception_immediately_reraised_without_retry`:** Uses a counting variable to verify `build_call_count == 1`, confirming no retry occurred.
