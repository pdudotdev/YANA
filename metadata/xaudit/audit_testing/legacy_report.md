# QA Audit Report — netKB Test Suite

**Audit type:** External QA review (automated test validity + coverage gap analysis)
**Scope:** `testing/automated/`, `testing/live/`, `testing/manual/`, CI pipeline
**Date:** 2026-03-27
**Auditor role:** Senior QA Architect (external)

---

## Executive Summary

The netKB test suite contains **~110 automated tests** across 10 suites (9 unit, 1 integration) plus **35 conditionally-executed live tests** and **10 manual scenarios**. The overall architecture is sound — tests are well-organized, mocking is generally appropriate, and security-critical input validation is tested with adversarial payloads.

However, the audit identified **3 ghost/silent pass conditions**, **3 mock false-pass risks**, **14 coverage gaps**, and **3 security test gaps**. Several of these are severity-high issues that could allow regressions to ship undetected.

### Verdict Summary

| Suite | ID | Tests | Verdict |
|-------|----|-------|---------|
| Input Model Validation | UT-001 | 17 | SOLID |
| Platform Map | UT-002 | 21 | SOLID |
| Tool Layer | UT-003 | 13 | GOOD — mock verification gap |
| Transport Dispatcher | UT-004 | 5 | SOLID |
| Vault Client | UT-005 | 5 | WEAK — missing happy path, fragile mock |
| Ingest Helpers | UT-006 | 10 | SOLID |
| NetBox Loader | UT-007 | 17 | EXCELLENT |
| SSH Layer | UT-008 | 11 | EXCELLENT |
| MCP Server Registration | UT-009 | 2 | MINIMAL — too thin |
| RAG Pipeline | IT-001 | 9 | CONDITIONAL — skip risk + weak assertion |
| Platform Coverage (live) | LT-001 | 35 | GOOD — EMPTY-as-pass concern |

---

## 1. Ghost Conditions and Silent Passes

Ghost conditions are tests that appear to verify functionality but pass regardless of whether the feature works correctly.

### 1.1 IT-001 `test_basic_query` — Trivially True Assertion

**File:** `testing/automated/test_rag_pipeline.py:32-34`
**Assertion:** `assert len(result["results"]) > 0`
**Problem:** This passes as long as ChromaDB returns *anything* for the query `"OSPF neighbor states"`. With a populated database containing dozens of chunks, this assertion is trivially true regardless of embedding model quality, query relevance, or retrieval accuracy. A broken embedding model returning random chunks would still pass this test.
**Severity:** HIGH — the only RAG quality gate is vacuous.
**Fix:** Assert that at least one result contains expected keywords (e.g., `"neighbor"`, `"adjacency"`, `"FULL"`) in its content field.

### 1.2 LT-001 `classify()` — EMPTY Output Passes

**File:** `testing/live/test_platform_coverage.py:28-45, 124, 133`
**Assertion:** `assert status != "FAIL"` — meaning both PASS and EMPTY are accepted.
**Problem:** A command that returns zero output (empty string or whitespace) is classified as EMPTY, which passes the assertion. If a device silently swallows a command and produces no output (e.g., due to privilege misconfiguration or platform bug), the test passes. This masks a real operational failure.
**Severity:** MEDIUM — conscious design choice, but could hide issues in a live environment.
**Fix:** Either assert `status == "PASS"` (strict) or log EMPTY results as warnings with a count threshold that fails the suite if too many are EMPTY.

### 1.3 IT-001 Entire Suite — Silently Skippable

**File:** `testing/automated/test_rag_pipeline.py:8-11`
**Condition:** `pytestmark = pytest.mark.skipif(not CHROMA_DIR.exists(), ...)`
**Problem:** All 9 RAG pipeline tests are silently skipped if `data/chroma/` does not exist. In CI, this is mitigated by running `python ingest.py` before tests. But locally, a developer running `pytest testing/automated/` without prior ingestion gets 9 silent skips — potentially believing they have full coverage when the entire RAG test suite is inactive.
**Severity:** MEDIUM — mitigated in CI, but misleading locally.
**Fix:** Add a CI step that fails if any tests were unexpectedly skipped. Locally, consider a conftest warning.

---

## 2. Mock Fidelity Analysis

Mocks that are too permissive can cause tests to pass even when the code under test is broken.

### 2.1 UT-003 — SSH Mock Never Verified

**File:** `testing/automated/test_tools.py:31-37, 41-44, 47-50`
**Problem:** `transport.execute_ssh` is mocked with `AsyncMock` across 6 tests. The mock's `return_value` is consumed to build the result dict, but `mock_ssh.assert_called_with(...)` or `mock_ssh.assert_called_once()` is **never used**. This means:
- If `get_ospf` stopped calling `execute_ssh` entirely and hardcoded a result, tests would pass.
- If `get_ospf` passed the wrong device dict or wrong command string to `execute_ssh`, tests would pass.
- The tests verify result dict assembly, not the contract between tool layer and transport layer.

**Severity:** HIGH — a regression in argument passing to SSH would go undetected.
**Fix:** Add `mock_ssh.assert_called_once()` and verify `mock_ssh.call_args` includes the expected device dict and resolved command string in at least the primary test cases.

### 2.2 UT-005 — Fragile MagicMock Auto-Chaining on hvac

**File:** `testing/automated/test_vault.py:62-68`
**Problem:** The Vault failure test patches `sys.modules` with `{"hvac": MagicMock()}`, then sets:
```python
hvac.Client.return_value.secrets.kv.v2.read_secret_version.side_effect = Exception("unreachable")
```
This works because MagicMock auto-creates attributes on access. However, if `vault.py` changes its call chain (e.g., to `client.logical.read()` or a different API version), MagicMock would silently return a new MagicMock for the new chain — the `side_effect` on the old chain would never fire, and the test would exercise a completely different code path than intended. **The test would pass without ever triggering the exception.**
**Severity:** HIGH — a vault.py refactor would silently break test intent.
**Fix:** Use `spec=True` on the mock or explicitly set `hvac.Client.return_value.logical = MagicMock(spec=[])` to make unexpected attribute access raise `AttributeError`.

### 2.3 UT-005 — No Happy-Path Vault Test

**File:** `testing/automated/test_vault.py` (entire file)
**Problem:** There are 5 Vault tests covering: no env vars, cache hit, cache miss fallback, and failure sentinel. But there is **no test for the happy path**: Vault is available → hvac client connects → API returns secret data → cache is populated → correct value is returned. The `test_cache_hit` test seeds the cache manually (`core.vault._cache["test/path"] = {"username": "admin"}`) so it never tests that Vault responses actually get parsed and cached.
**Severity:** HIGH — the most important code path (successful credential retrieval) is untested.
**Fix:** Add a test that mocks a successful `hvac.Client().secrets.kv.v2.read_secret_version()` return value and verifies: (1) the correct value is returned, (2) the cache is populated, (3) a second call returns from cache without calling hvac again.

---

## 3. Coverage Gap Inventory

Features and code paths that have no automated test coverage.

### 3.1 HIGH Priority

| # | Gap | Source Location | Risk |
|---|-----|----------------|------|
| G-01 | RAG retrieval relevance/quality | `tools/rag.py:57` | Broken embeddings or retrieval produce garbage results undetected |
| G-02 | MCP tool schema validation | `server/MCPServer.py:22-24` | Schema changes (parameter types, descriptions, required fields) go undetected |
| G-03 | Vault happy-path (successful read + cache population) | `core/vault.py:25-36` | Most critical credential path untested |
| G-04 | SSH mock argument verification in tool layer | `tools/ospf.py:29`, `tools/operational.py:23` | Wrong arguments passed to SSH go undetected |

### 3.2 MEDIUM Priority

| # | Gap | Source Location | Risk |
|---|-----|----------------|------|
| G-05 | Semaphore concurrency limiting | `transport/__init__.py:11,21` | Semaphore misconfiguration allows unbounded SSH connections |
| G-06 | VyOS live test coverage | `testing/live/test_platform_coverage.py:15-21` | VyOS is the only supported CLI style with zero live validation |
| G-07 | `transport.execute_command` with `timeout_ops` parameter | `transport/__init__.py:15` | Non-default timeout path never exercised |
| G-08 | RAG `$and` compound filter construction (unit test) | `tools/rag.py:48-49` | Filter wrapping logic only tested via integration with real ChromaDB |
| G-09 | `core/settings.py` import-time credential loading | `core/settings.py:6-7` | Module-level `get_secret()` calls during import could fail silently |
| G-10 | `core/inventory.py` import-time `load_devices()` failure | `core/inventory.py` | Import-time side effect failure not tested |

### 3.3 LOW Priority

| # | Gap | Source Location | Risk |
|---|-----|----------------|------|
| G-11 | Ingest error handling (malformed files, write failures) | `ingest.py:130-177` | Ingestion silently produces corrupt DB |
| G-12 | `_error_response("", msg)` — empty string device | `tools/__init__.py:7` | `if device:` treats `""` as falsy; minor edge case |
| G-13 | MCP server `.env` loading | `server/MCPServer.py:11` | Environment not loaded → credentials missing |
| G-14 | `run_tests.sh` fragile grep-based pass/fail detection | `testing/run_tests.sh:26-31` | Test names containing "failed" or "skipped" misclassify suite results |

---

## 4. Security Test Gaps

### 4.1 VRF Injection — Unicode and Encoded Characters

**Tested:** ASCII metacharacters (`;`, `|`, space, overlength, empty string) — 5 payloads in `test_input_models.py:22-31`.
**Not tested:** Unicode homoglyphs (e.g., `VRF\u037e` which is a Greek question mark that looks like `;`), zero-width characters (`\u200b`), URL-encoded payloads (`VRF%3Bdrop`), or null bytes (`VRF\x00;drop`).
**Risk:** The regex `^[a-zA-Z0-9_-]{1,32}$` should reject all of these because they don't match `[a-zA-Z0-9_-]`, but this is a security-critical assumption that deserves explicit test coverage.
**Severity:** LOW — the regex is correct, but defense-in-depth requires verification.

### 4.2 Adversarial KB Query Strings

**Tested:** None. `KBQuery.query` is tested for max-length boundary (500/501 chars) but not for adversarial content.
**Not tested:** ChromaDB filter injection attempts (e.g., queries containing `$and`, `$or`, `$not` operators), extremely repetitive token floods, or queries designed to maximize embedding computation time.
**Risk:** The query string is passed to `vs.similarity_search(params.query, ...)` which goes through the embedding model. Adversarial inputs could cause unexpected behavior in HuggingFace embeddings or ChromaDB.
**Severity:** LOW — ChromaDB's `similarity_search` does not interpret query text as filter syntax, but computational DoS via crafted queries is theoretically possible.

### 4.3 Device Name Sanitization in Error Messages

**Tested:** Adversarial device names (injection strings, overlength, empty) produce clean error dicts — `test_tools.py:86-97`.
**Not tested:** The error message includes the raw device name: `f"Unknown device: {params.device}"`. If error responses are ever rendered in a web UI, this is an XSS vector. No test verifies that device names are sanitized or escaped in error output.
**Risk:** Low in current architecture (MCP stdio transport, LLM-consumed responses). Would become high if a web dashboard is added.
**Severity:** LOW (current), HIGH (if architecture changes).

---

## 5. Test Infrastructure Issues

### 5.1 `run_tests.sh` — Fragile Pass/Fail Detection

**File:** `testing/run_tests.sh:26-36`
**Problem:** Suite-level pass/fail is determined by grepping pytest output:
```bash
if echo "$output" | grep -qE "failed"; then
    # → FAIL
elif echo "$output" | grep -q "skipped"; then
    # → SKIP
else
    # → PASS
fi
```
If a test *name* contains the word "failed" (e.g., `test_vault_failure_returns_failed_status`), the script classifies the entire suite as FAIL even if all tests passed. Similarly, "skipped" in a test name triggers false SKIP.
**Severity:** MEDIUM — currently no test names trigger this, but it's a latent defect.
**Fix:** Parse pytest's exit code instead of grepping output text. Pytest returns 0 for all-pass, 1 for failures, 5 for no tests collected.

### 5.2 `conftest.py` — Incomplete Inventory Patching

**File:** `testing/automated/conftest.py:25-33`
**Problem:** The `mock_inventory` fixture patches `devices` on exactly 4 modules: `core.inventory`, `tools.ospf`, `tools.operational`, `transport`. If a future module imports `devices` from `core.inventory`, it will NOT be patched, potentially causing tests to hit the real NetBox inventory or fail with import-time errors.
**Severity:** LOW (current), MEDIUM (as codebase grows).
**Fix:** Consider making `core.inventory.devices` a function call (`get_devices()`) that reads from a module-level variable, making it patchable in one place. Or add a CI check that greps for `from core.inventory import devices` and verifies all import sites are listed in conftest.

### 5.3 CI Pipeline — No Skip Threshold

**File:** `.github/workflows/ci.yml:41`
**Problem:** The CI command `python -m pytest testing/automated/ -v --tb=short --timeout=30` will pass even if the RAG pipeline tests (IT-001, 9 tests) are silently skipped. There is no assertion that the expected number of tests actually ran.
**Severity:** MEDIUM — a broken CI step (e.g., `ingest.py` fails silently) could cause 9 tests to skip without failing the pipeline.
**Fix:** Add `--strict-markers` or a post-test step that checks `pytest --co -q | wc -l` against an expected minimum.

---

## 6. Per-Suite Detailed Verdicts

### UT-001: Input Model Validation — SOLID

17 tests covering all Pydantic models (`OspfQuery`, `InterfacesQuery`, `KBQuery`). Includes boundary tests (500/501 chars, 0/11 top_k), injection payloads (5 VRF attacks), JSON parsing, and enum rejection. Every assertion is substantive. No ghost conditions.

**One gap:** `TestInterfacesQuery` has only 1 test (`test_valid`). While `InterfacesQuery` only has a `device: str` field with no constraints beyond being a string, the asymmetry with the thorough `TestOspfQuery` and `TestKBQuery` classes is notable.

### UT-002: Platform Map — SOLID

21 tests covering structure completeness, VRF resolution (`_apply_vrf` with 5 edge cases), `get_action` integration (3 vendors), error paths (unknown cli_style, unknown category), and VRF override semantics. Clean, thorough, no mocks needed (pure functions).

### UT-003: Tool Layer — GOOD

13 tests covering `_error_response`, `get_ospf` (4 tests), `get_interfaces` (3 tests), VRF end-to-end (1 test), and adversarial device names (4 parametrized payloads). Good security coverage with injection strings.

**Weakness:** SSH mock is never verified with `assert_called_with`. Tests prove result dict assembly but not the tool-to-transport contract. See Section 2.1.

### UT-004: Transport Dispatcher — SOLID

5 tests covering unknown device, success path, error dict shapes (2 different shapes for unknown-device vs SSH-failure), and error message propagation. Exact dict shape assertions prevent field leakage.

### UT-005: Vault Client — WEAK

5 tests covering env fallback (2), cache hit, cache miss, and failure sentinel. All assertions are substantive (no ghost conditions), but:
- Missing happy-path test (successful Vault read → cache populated). See Section 2.3.
- Fragile MagicMock auto-chaining on hvac. See Section 2.2.
- No test for Vault cache TTL behavior (there is none — permanent cache, which is itself a concern).

### UT-006: Ingest Helpers — SOLID

10 tests covering metadata extraction (5 vendor files + RFC + unknown), network context loading (NetBox intent, fallback to JSON, inventory metadata), and `_router_to_markdown` (3 router configurations). Uses `tmp_path` and `monkeypatch` correctly.

**Minor gap:** No test for malformed INTENT.json or corrupted markdown files.

### UT-007: NetBox Loader — EXCELLENT

17 tests covering `load_devices` (10 tests) and `load_intent` (7 tests). Extensive error path coverage: missing URL, missing token, API exception, empty results, missing fields, per-device exceptions. Helper functions `_make_nb_device` and `_make_pynetbox` are well-constructed and mirror pynetbox's API surface. The strongest test file in the suite.

### UT-008: SSH Layer — EXCELLENT

11 tests covering `_build_cli` (7 tests: MikroTik username suffix, return char, transport selection for standard/VyOS, Vault credential hierarchy, global fallback) and `execute_ssh` (4 tests: success, OpenException no-retry, transient retry+recover, all retries exhausted). Custom async context manager helpers (`_async_cm`, `_failing_cm`) are well-built. Retry behavior is verified with call counters.

### UT-009: MCP Server Registration — MINIMAL

2 tests: tool count (3) and tool name set. This verifies the registration contract but nothing else.

**Missing:**
- Tool parameter schema validation (types, descriptions, required fields)
- Tool invocation via MCP protocol dispatch
- Error handling during tool execution
- Tool description/docstring presence

### IT-001: RAG Pipeline — CONDITIONAL

9 tests covering basic query, metadata structure, vendor filter, topic filter, compound filter, intent topic, vectorstore failure, and top_k limiting. Good filter enforcement tests. The error path test (`test_vectorstore_failure_returns_error_dict`) is well-constructed.

**Critical issue:** `test_basic_query` has a vacuous assertion. See Section 1.1.
**Critical issue:** Entire suite is silently skippable. See Section 1.3.

### LT-001: Platform Coverage — GOOD

35 tests (5 vendors x 7 queries) against live devices. Correct gating via `--live` flag. Report generation fixture is useful. `classify()` function handles vendor-specific error indicators.

**Issue:** EMPTY-as-pass classification. See Section 1.2.
**Gap:** VyOS (6th supported CLI style) absent from live tests.

---

## 7. Feature-to-Test Traceability Matrix

| Feature | Tested By | Coverage Level |
|---------|-----------|---------------|
| OspfQuery Literal enum validation | UT-001 (6+1 tests) | Full |
| VRF regex validation | UT-001 (5 injection payloads) | Good (ASCII only) |
| KBQuery max_length / top_k bounds | UT-001 (4 boundary tests) | Full |
| JSON string pre-parsing (BaseParamsModel) | UT-001 (3 tests) | Full |
| Platform map structure completeness | UT-002 (3 structural tests) | Full |
| VRF resolution + override semantics | UT-002 (7 tests) + UT-003 (2 tests) | Full |
| Tool layer device lookup | UT-003 (2 unknown-device tests) | Good |
| Tool layer adversarial device names | UT-003 (4 parametrized payloads) | Good |
| Transport dispatcher error shapes | UT-004 (3 shape tests) | Full |
| SSH semaphore concurrency limiting | None | **Not tested** |
| Vault env fallback | UT-005 (2 tests) | Good |
| Vault cache + sentinel | UT-005 (3 tests) | Partial (no happy path) |
| Vault successful read | None | **Not tested** |
| NetBox device loading + error paths | UT-007 (10 tests) | Full |
| NetBox intent loading + prefix fallback | UT-007 (7 tests) | Full |
| Ingest metadata extraction | UT-006 (5+2 tests) | Full |
| Ingest network context fallback | UT-006 (3 tests) | Good |
| SSH _build_cli per-platform logic | UT-008 (7 tests) | Full |
| SSH retry logic + OpenException | UT-008 (4 tests) | Full |
| MCP tool registration | UT-009 (2 tests) | Minimal |
| MCP tool schemas | None | **Not tested** |
| MCP tool invocation via protocol | None | **Not tested** |
| RAG vector search | IT-001 (9 tests) | Conditional |
| RAG filter enforcement | IT-001 (4 filter tests) | Good (when DB exists) |
| RAG retrieval relevance | None | **Not tested** |
| RAG $and filter construction | IT-001 only (no unit test) | Weak |
| Live multi-vendor SSH | LT-001 (35 tests) | Good (5/6 vendors) |
| VyOS live SSH | None | **Not tested** |
| Static command map (no run_show) | By design (no tool exists) | N/A |
| Read-only policy | Manual test #7 | Manual only |
| Data boundary (prompt injection) | Manual test (behavioral) | Manual only |

---

## 8. Prioritized Recommendations

### P0 — Fix Before Next Release

1. **Add SSH mock call verification to UT-003.** In `test_valid_device_ios` (both ospf and interfaces), add `mock_ssh.assert_called_once()` and verify `mock_ssh.call_args` contains the expected device dict and resolved command string. This closes the tool-to-transport contract gap.

2. **Add Vault happy-path test to UT-005.** Mock a successful `hvac.Client().secrets.kv.v2.read_secret_version()` return, verify: correct value returned, cache populated, second call returns from cache without calling hvac again.

3. **Strengthen IT-001 `test_basic_query`.** Replace `len(result["results"]) > 0` with an assertion that at least one result's `content` field contains a relevant keyword (e.g., `any("neighbor" in r["content"].lower() for r in result["results"])`).

4. **Fix UT-005 hvac mock fragility.** Replace `MagicMock()` with a mock that uses `spec` or explicitly raises on unexpected attribute access, so vault.py refactors are caught.

### P1 — Address in Next Sprint

5. **Add MCP tool schema tests to UT-009.** Verify each tool's parameter schema: types, required fields, descriptions, and that schemas match the Pydantic models.

6. **Add VyOS to live test suite (LT-001).** If a VyOS device is available in the lab topology, add it to `TEST_DEVICES`. If not, document why it's excluded.

7. **Add CI skip threshold.** Add a post-test step that verifies the expected number of tests ran, or use `pytest --strict-markers` to prevent silent skips.

8. **Fix `run_tests.sh` pass/fail detection.** Replace text-grepping with pytest exit code parsing: `$? == 0` → PASS, `$? == 1` → FAIL, `$? == 5` → SKIP (no tests collected).

### P2 — Backlog

9. **Add semaphore concurrency test.** Launch N > 5 concurrent `execute_command` calls with a mock SSH that tracks active connections, verify peak concurrency equals `SSH_MAX_CONCURRENT`.

10. **Add RAG filter construction unit test.** Test `search_knowledge_base` with mocked `_get_vectorstore` to verify the `where` dict is built correctly for: no filter, vendor-only, topic-only, and compound vendor+topic.

11. **Add Unicode VRF injection payloads.** Extend `test_vrf_injection_rejected` with: `"VRF\u037e"` (Greek question mark), `"VRF\u200b"` (zero-width space), `"VRF\x00"` (null byte).

12. **Add transport `timeout_ops` test.** Call `execute_command` with an explicit timeout and verify it's passed through to `execute_ssh`.

13. **Add ingest error handling tests.** Test malformed INTENT.json, corrupt markdown, and ChromaDB write failure scenarios.

14. **Consider LT-001 EMPTY threshold.** Add a configurable threshold (e.g., fail if >20% of results are EMPTY) to catch platforms that silently produce no output.

---

## Appendix A: Test Inventory

| ID | Suite | File | Count | Type |
|----|-------|------|-------|------|
| UT-001 | Input Model Validation | `test_input_models.py` | 17 | Unit |
| UT-002 | Platform Map | `test_platform_map.py` | 21 | Unit |
| UT-003 | Tool Layer | `test_tools.py` | 13 | Unit |
| UT-004 | Transport Dispatcher | `test_transport.py` | 5 | Unit |
| UT-005 | Vault Client | `test_vault.py` | 5 | Unit |
| UT-006 | Ingest Helpers | `test_ingest.py` | 10 | Unit |
| UT-007 | NetBox Loader | `test_netbox.py` | 17 | Unit |
| UT-008 | SSH Layer | `test_ssh.py` | 11 | Unit |
| UT-009 | MCP Server Registration | `test_mcp_server.py` | 2 | Unit |
| IT-001 | RAG Pipeline | `test_rag_pipeline.py` | 9 | Integration |
| LT-001 | Platform Coverage | `test_platform_coverage.py` | 35 | Live |
| MT-001–010 | Manual Scenarios | `manual_tests.md` | 10 | Manual |

**Total automated:** ~110 (unit) + 9 (integration) + 35 (live, conditional)
**Total manual:** 10

## Appendix B: Source Files Reviewed

Every source file was read line-by-line as part of this audit:

- `server/MCPServer.py` (28 lines)
- `tools/__init__.py` (10 lines), `tools/ospf.py` (30 lines), `tools/operational.py` (24 lines), `tools/rag.py` (68 lines)
- `transport/__init__.py` (34 lines), `transport/ssh.py` (76 lines)
- `core/vault.py` (42 lines), `core/netbox.py` (121 lines), `core/settings.py` (14 lines), `core/inventory.py`
- `input_models/models.py` (56 lines)
- `platforms/platform_map.py`
- `ingest.py` (178 lines)
- All test files under `testing/` (listed in Appendix A)
- `testing/run_tests.sh` (81 lines)
- `testing/automated/conftest.py` (34 lines), `testing/live/conftest.py` (50 lines)
- `.github/workflows/ci.yml` (78 lines)
