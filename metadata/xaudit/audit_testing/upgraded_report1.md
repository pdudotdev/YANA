# YANA Test Quality Audit Report

**Scope:** Full
**Date:** 2026-03-27
**Test files reviewed:** 10 (automated) + 1 (live) + conftest.py
**Total test functions reviewed:** 64 (53 automated unit/integration + 11 parametrized live)

---

## Executive Summary

The YANA test suite is above average for a project of this size — most tests have specific assertions, and the conftest mock inventory design is sound. However, the audit identified **two S1 ghost passes** where tests pass regardless of whether the function under test works correctly, **three S2 mock infidelity issues** that could mask real integration failures, and **seven S3 coverage gaps** in critical code paths including `core/settings.py`, `core/inventory.py`, and the main `ingest()` function. The most critical theme is that the tool layer tests (`test_tools.py`) have a structural mock-leakage problem: `get_ospf()` and `get_interfaces()` are thin wrappers around `execute_command()`, and when `execute_ssh` is mocked, the mock's return value flows through both functions without transformation, making several assertions test the mock rather than the function logic.

---

## Findings by Severity

### S1 — Ghost Passes

1. **S1-001** — `test_tools.py::TestGetInterfaces::test_valid_device_ios` — `assert "raw" in result` is loose enough to pass if the function returned any dict containing a "raw" key, including a hardcoded error dict.
2. **S1-002** — `test_tools.py::TestAdversarialDeviceName::test_adversarial_name_returns_clean_error` — Tests assert only `"error" in result` with no assertion on error message content, and have no assertion that the function did NOT execute a command. The empty-string parametrize case (`""`) is particularly suspect — Pydantic allows empty string for `device: str`, and the function simply does a dict lookup that returns `None` for `""`, producing an error dict. The test verifies nothing specific.

### S2 — Mock Infidelity

1. **S2-001** — `execute_ssh` mock returns `str`, but real `execute_ssh` returns `str` (from `result.result`). The mock in `_async_cm` returns a `MagicMock` with `.result` attribute correctly, so `test_ssh.py` is accurate. However, in `test_tools.py` and `test_transport.py`, `execute_ssh` is patched to return a plain string directly — this is correct because the real function does return `str`. **Downgraded to observation — no actual infidelity.**
2. **S2-002** — `MOCK_DEVICES` keys vs real `load_devices()` output — MOCK_DEVICES uses `{host, platform, cli_style, vrf?}` which matches the real `load_devices()` return shape exactly. **No infidelity.**
3. **S2-003** — `test_ssh.py::TestBuildCli` — Tests assert on `mock_cli.call_args.kwargs["auth_options"]` attributes (`.username`, `.password`). The real `AuthOptions` is a Scrapli dataclass. Because `_build_cli` constructs a real `AuthOptions(username=..., password=...)` object and passes it to the mocked `Cli`, the assertions check the real `AuthOptions` object, not a mock. **This is actually correct and well-designed.**
4. **S2-004** — `test_rag_pipeline.py` mocks `_get_vectorstore` with `side_effect=RuntimeError` for the error test. The real error path catches `Exception`, so `RuntimeError` is appropriate. However, the test returns `{"error": "Knowledge base unavailable: ..."}` which matches the real code. **No infidelity.**
5. **S2-005** — `test_vault.py::test_vault_failure_sets_sentinel` — The mock chain `hvac.Client.return_value.secrets.kv.v2.read_secret_version.side_effect = Exception("unreachable")` simulates Vault being unreachable. However, the real code does `import hvac; client = hvac.Client(url=vault_addr, token=vault_token)` and then calls the method. The test patches `sys.modules["hvac"]` with a `MagicMock()`, which means `import hvac` inside `get_secret()` gets the mock module. This works because Python's `import` returns the cached `sys.modules` entry. The mock chain accurately reaches the same attribute path as real code. However, the `hvac.Client.return_value` mock means the mock module-level `Client` class's return value (the mock client instance) has `secrets.kv.v2.read_secret_version.side_effect` set. If the real code instantiates `hvac.Client()`, it gets `Client.return_value`, which is the mock instance. This is correct. **No infidelity, but fragile — relies on MagicMock auto-creation behavior.**

After rigorous analysis, the actual S2 findings reduce to:

1. **S2-001** — `conftest.py` `autouse=True` mock_inventory — it patches `core.inventory.devices`, `tools.ospf.devices`, `tools.operational.devices`, and `transport.devices`. However, `test_rag_pipeline.py` tests the RAG pipeline which does NOT use the inventory at all. The autouse fixture runs unnecessarily for these tests. More critically, `test_mcp_server.py` imports `server.MCPServer` which imports `tools.ospf`, `tools.operational`, and `tools.rag`. The mock inventory replaces the `devices` dict AFTER the module-level import in `core.inventory` has already run (and failed, setting `devices = {}`). The conftest then overwrites the empty dict with MOCK_DEVICES. This works for testing but masks a real import-time failure scenario.
2. **S2-002** — `test_netbox.py` `_make_nb_device` helper creates mock pynetbox device objects with `dev.custom_fields = {"cli_style": cli_style, "vrf": vrf}`. The real code accesses `(dev.custom_fields or {}).get("cli_style", "")`. This matches. However, the real `dev.platform.slug` is accessed — the mock uses `dev.platform = MagicMock()` then `dev.platform.slug = platform_slug`, which correctly returns the string. **Accurate mock.**
3. **S2-003** — `test_vault.py::test_vault_failure_sets_sentinel` — The mock Vault client chain is structurally correct but extremely fragile. If the real `hvac` library changes its API path from `client.secrets.kv.v2.read_secret_version()` to something else, the mock would silently succeed (MagicMock auto-creates any attribute), and the test would still pass but no longer test the real code path. This is a latent infidelity risk.

### S3 — Coverage Gaps

1. **S3-001** — `core/settings.py` — No test file. The import-time `get_secret()` calls for `USERNAME` and `PASSWORD`, and all constant values (`SSH_TIMEOUT_OPS`, `SSH_RETRIES`, `SSH_RETRY_DELAY`, `SSH_MAX_CONCURRENT`) are untested. A bug like `SSH_RETRIES = -1` would cause `range(0)` in `execute_ssh`, meaning the loop body never executes and `last_exc` remains `None`, leading to `raise None` → `TypeError` at runtime. No test catches this.
2. **S3-002** — `core/inventory.py` — No direct test. The import-time `load_devices()` call and the fallback to `devices = {}` when NetBox is unavailable is only tested indirectly via conftest's monkeypatch. If the import-time call raises an unhandled exception (instead of returning `None`), the server crashes at startup. No test verifies this behavior.
3. **S3-003** — `ingest.py::ingest()` main function — Not tested. The chunking logic, embedding, ChromaDB write, and `--clean` flag are all untested. A bug in chunk metadata propagation (line 158: `chunk.metadata = doc.metadata.copy()`) would silently corrupt all KB metadata, causing filter queries to return wrong results. No test catches this.
4. **S3-004** — `server/MCPServer.py` tool invocation — Only registration count and names are tested. No test verifies that invoking a tool through the FastMCP protocol actually calls the underlying function correctly. If the `mcp.tool(name=...)(func)` decorator silently failed to wire up the function, the registration test would still pass (tool names registered) but invocations would fail.
5. **S3-005** — `transport/__init__.py` semaphore behavior — `_cmd_sem = asyncio.Semaphore(SSH_MAX_CONCURRENT)` is created at import time. No test verifies that concurrent requests are actually limited to `SSH_MAX_CONCURRENT`, or that semaphore slot exhaustion produces a meaningful error rather than a hang.
6. **S3-006** — `tools/rag.py::_get_vectorstore()` lazy initialization — No unit test covers the lazy init path (only the IT-001 integration test, which is conditionally skipped). If `_get_vectorstore()` is called concurrently, the global state mutation (`_vectorstore = Chroma(...)`) could race. No test exercises this.
7. **S3-007** — `get_ospf()` and `get_interfaces()` KeyError path — When `get_action()` raises `KeyError` (unsupported query for a platform), both tools catch it and return an error dict. This path is tested in `test_platform_map.py::test_unknown_category_raises` at the `get_action` level, but NOT at the tool level. The tool's `except KeyError` handler that formats the error message is untested.

### S4 — Test Quality

1. **S4-001** — `test_tools.py::TestGetInterfaces::test_valid_device_ios` line 65: `assert "raw" in result` — This is a loose existence check. Should be `assert "GigabitEthernet0/0" in result["raw"]` or similar to verify the mock output flowed through.
2. **S4-002** — `test_tools.py::TestAdversarialDeviceName::test_adversarial_name_returns_clean_error` line 96-97: Only asserts `"error" in result`. Does not verify error message content, and the comment "No exception raised, no command executed" is not actually verified by any assertion.
3. **S4-003** — `test_mcp_server.py` has only 2 tests. Tool names are tested with a set comparison (good), but tool count is tested with `len(tools) == 3` which would break silently if a tool were renamed vs. removed.
4. **S4-004** — `test_netbox.py::test_valid_device_parsed_correctly` line 73: `assert result is not None` — This is loose. Should assert `isinstance(result, dict)` at minimum. (The subsequent assertions on line 74-78 are specific and good, so this is a minor style issue.)
5. **S4-005** — `test_transport.py::test_ssh_failure_error_shape` lines 35-36: Uses loose key-existence checks (`assert "device" in result`, `assert "cli_style" in result`) rather than verifying exact values. The companion test `test_ssh_error_returns_error_dict` (line 43-46) IS specific about values. Mild redundancy.
6. **S4-006** — `test_platform_map.py::test_vrf_from_device_fallback` line 77: `assert "VRF1" in result` — Asserts that "VRF1" appears anywhere in the result string. This is sufficient for its purpose but could match a false positive if the base command contained "VRF1" for an unrelated reason.
7. **S4-007** — No test verifies that `OspfQuery` rejects a missing `device` field, or that `InterfacesQuery` rejects a missing `device` field. Pydantic `Field(...)` makes these required, so validation would catch it, but there is no explicit test proving it.

---

## Finding Detail (S1 and S2 only)

### [S1-001] `test_valid_device_ios` in TestGetInterfaces — Loose "raw" existence check

- **Test:** `testing/automated/test_tools.py::TestGetInterfaces::test_valid_device_ios` (line 59-65)
- **Ghost condition:** Line 65: `assert "raw" in result`. This asserts only that the key "raw" exists in the result dict. It does NOT assert on the raw value content.
- **Proof:** If `get_interfaces()` were replaced with `return {"device": params.device, "cli_style": devices[params.device]["cli_style"], "raw": ""}`, the test would still pass. The mock SSH output `"GigabitEthernet0/0  up  up  10.0.0.1"` is never verified. Compare with `TestGetOspf::test_valid_device_ios` (line 37) which correctly asserts `assert "FULL" in result["raw"]` — the interfaces test lacks this equivalent.
- **Minimal fix:** Change `assert "raw" in result` to `assert "GigabitEthernet0/0" in result["raw"]` to verify the mock output actually arrived in the result.

**Self-challenge:** The other assertions on lines 63-64 (`result["device"] == "R1"` and `result["cli_style"] == "ios"`) DO verify specific values that come from the inventory lookup, NOT from the mock. These are real tests. Only the `"raw" in result` assertion is a ghost. Partial ghost — the test is not entirely vacuous, but the core payload assertion is loose. **Verdict: Confirmed S1 for the payload assertion specifically. The test provides false confidence that the SSH output is correctly returned.**

### [S1-002] `test_adversarial_name_returns_clean_error` — No content assertion on error

- **Test:** `testing/automated/test_tools.py::TestAdversarialDeviceName::test_adversarial_name_returns_clean_error` (lines 87-97)
- **Ghost condition:** Line 96: `assert "error" in result`. For all 4 parametrized cases, the test only checks that the result dict contains an `"error"` key. It does not verify the error message content (e.g., `"Unknown device"`) or that no SSH command was executed.
- **Proof:** If `get_ospf()` were replaced with `return {"error": "completely wrong message"}` for all inputs, every parametrized case would still pass. The test cannot distinguish between the correct error path ("Unknown device: ...") and a completely different error.
- **Minimal fix:** Add `assert "Unknown device" in result["error"]` after the existing assertion. Also add `mock_ssh.assert_not_called()` to verify no command was executed (would require patching `transport.execute_ssh`).

**Self-challenge:** The purpose of this test is to verify that adversarial device names don't cause exceptions (crashes, injection). The `assert "error" in result` does confirm the function returned an error dict rather than crashing. However, it does NOT confirm that the error came from the inventory lookup rather than some other unrelated error (e.g., a `TypeError` from the adversarial string being processed further down). The fact that no mock is in place for `execute_ssh` means if the adversarial name somehow passed the inventory lookup, the test would hit a real `execute_ssh` call which would fail with a different error — and the test would still pass. **Verdict: Confirmed S1. The test cannot distinguish between the intended error path and an accidental error from a different cause.**

### [S2-001] `conftest.py` `autouse=True` mock_inventory — unnecessary for RAG and MCP tests

- **Mock:** `testing/automated/conftest.py::mock_inventory` (lines 22-33), `autouse=True`
- **Real function:** `core.inventory.devices` is populated at import time by `load_devices()`. The conftest overwrites it in 4 module namespaces.
- **Structural diff:** Not a shape mismatch — the mock dict structure matches the real output. The issue is that autouse applies the mock to ALL tests, including `test_rag_pipeline.py` and `test_mcp_server.py`, which don't need or use the device inventory for their assertions.
- **Impact:** Minor. For `test_rag_pipeline.py`, the mock is harmless — RAG tests don't query devices. For `test_mcp_server.py`, the mock ensures the `mcp` object can be imported without a live NetBox connection, which is actually necessary. **Downgrade from S2 to observation.** The autouse is justified for ensuring all tests can run without NetBox, but it hides the import-time failure scenario.

### [S2-003] `test_vault.py::test_vault_failure_sets_sentinel` — fragile mock chain

- **Mock:** `test_vault.py` line 62-64: `patch.dict("sys.modules", {"hvac": MagicMock()})` followed by `hvac.Client.return_value.secrets.kv.v2.read_secret_version.side_effect = Exception("unreachable")`
- **Real function:** `core/vault.py` lines 26-32: `import hvac; client = hvac.Client(url=vault_addr, token=vault_token); response = client.secrets.kv.v2.read_secret_version(path=path, ...)`
- **Structural diff:** The mock relies on MagicMock's auto-attribute creation to mirror the `hvac` library's API chain. If `hvac` ever changes its API (e.g., `client.secrets.kv.v2` becomes `client.kv_v2`), the mock would auto-create the new path without raising an error, and the test would silently test the wrong code path.
- **Impact:** Low probability — `hvac` is a mature library. But the pattern of using MagicMock for deep attribute chains is inherently fragile. A `spec=` argument on the mock would catch API changes. **Confirmed S2, low severity.**

---

## Coverage Matrix

| Source Module | Test File | Functions Tested | Functions NOT Tested | Critical Gap? |
|---------------|-----------|-----------------|----------------------|---------------|
| `core/settings.py` | **NONE** | (none) | `USERNAME`, `PASSWORD` load path, all SSH constants | Y (S3-001) |
| `core/vault.py` | `test_vault.py` | `get_secret()` — 5 scenarios: no vault env, no fallback, cache hit, cache missing key, vault failure sentinel | `get_secret()` success path with real Vault response (only tested via mock), `quiet` parameter logging behavior | N |
| `core/netbox.py` | `test_netbox.py` | `load_devices()` — 8 scenarios; `load_intent()` — 5 scenarios | (comprehensive) | N |
| `core/inventory.py` | **NONE** (indirect) | `devices` dict replaced by conftest | Import-time `load_devices()` call, fallback to empty dict, exception during import | Y (S3-002) |
| `transport/__init__.py` | `test_transport.py` | `execute_command()` — 5 scenarios: unknown device, success, error shapes, SSH failure | `_cmd_sem` semaphore behavior, concurrent slot limits | Y (S3-005) |
| `transport/ssh.py` | `test_ssh.py` | `_build_cli()` — 6 scenarios; `execute_ssh()` — 4 scenarios incl. retry, OpenException, exhaustion | (comprehensive for its scope) | N |
| `platforms/platform_map.py` | `test_platform_map.py` | `PLATFORM_MAP` structure, `_apply_vrf()` — 5 cases, `get_action()` — 7 cases | (comprehensive) | N |
| `input_models/models.py` | `test_input_models.py` | `OspfQuery` — 7 tests, `InterfacesQuery` — 1 test, `KBQuery` — 7 tests | Missing required field rejection for `OspfQuery.device` and `InterfacesQuery.device` | N (Pydantic enforces) |
| `tools/__init__.py` | `test_tools.py` | `_error_response()` — 2 tests | (complete) | N |
| `tools/ospf.py` | `test_tools.py` | `get_ospf()` — 5 tests + 4 adversarial | `get_ospf()` KeyError path (unsupported query for platform) | N (low risk) |
| `tools/operational.py` | `test_tools.py` | `get_interfaces()` — 3 tests | `get_interfaces()` KeyError path | N (low risk) |
| `tools/rag.py` | `test_rag_pipeline.py` (IT, conditional skip) | `search_knowledge_base()` — 8 tests + 1 error path | `_get_vectorstore()` lazy init, concurrent access race | Y (S3-006, if running without ChromaDB) |
| `server/MCPServer.py` | `test_mcp_server.py` | Tool registration (count=3, names match) | Tool invocation through FastMCP, server startup, error middleware | Y (S3-004) |
| `ingest.py` | `test_ingest.py` | `extract_metadata()` — 5 tests, `_router_to_markdown()` — 3 tests, `load_network_context()` — 3 tests | `ingest()` main function: chunking, embedding, ChromaDB write, `--clean` flag | Y (S3-003) |

---

## CI Cross-Check

| Check | Status | Notes |
|-------|--------|-------|
| All tests pass in CI | UNKNOWN | Cannot run CI; analysis based on code review only |
| No unjustified skips | PASS | IT-001 skip condition (`data/chroma/` not exists) is justified. CI runs `python ingest.py` before tests, creating the directory. Locally, it may not exist. The `pytestmark = pytest.mark.skipif(not CHROMA_DIR.exists(), ...)` is correctly implemented at module level, evaluated at collection time. |
| Timeout (30s) appropriate | PASS | All automated tests are mocked and should complete in <1s. IT-001 (RAG pipeline) requires embedding model load which could be slow on first run, but 30s should suffice for a cached model. |
| run_tests.sh vs CI parity | FAIL | CI runs `python -m pytest testing/automated/ -v --tb=short --timeout=30` (single invocation, collects all tests). `run_tests.sh` runs per-file (`pytest testing/automated/test_X.py`). Divergence: (1) CI has a 30s timeout per test, local does not. (2) CI collects all test files in one session, so conftest fixtures are shared across all files. Local runs each file in isolation, so any fixture-isolation bugs would manifest differently. (3) CI result is a single pass/fail, local classifies per-file via grep on output. |
| VyOS in live coverage | ABSENT | VyOS (`R6`) is in `MOCK_DEVICES` and `PLATFORM_MAP`, but not in `TEST_DEVICES` in `test_platform_coverage.py`. This appears intentional — likely no VyOS device exists in the lab. The platform map IS tested structurally (all 6 cli_styles verified in `test_platform_map.py::test_all_vendors_present` and `test_ospf_queries_complete`), but live command execution against a VyOS device is never validated. |

### Skip Audit Detail

**IT-001 (`test_rag_pipeline.py`):**
- Skip condition: `pytest.mark.skipif(not CHROMA_DIR.exists(), reason="ChromaDB not populated")`
- `CHROMA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "chroma"`
- In CI: `python ingest.py` runs before tests, creating `data/chroma/`. Skip should NOT trigger in CI.
- Locally: If `data/chroma/` does not exist, all 10 tests in this file are skipped. This is correct behavior.
- **Risk:** The skip is evaluated at module collection time via `pytestmark`. If `ingest.py` fails silently in CI (e.g., no docs found, exits with code 1), the directory wouldn't be created and all RAG tests would be silently skipped. CI step does NOT check `ingest.py` exit code explicitly — the step would fail and stop the job due to GitHub Actions default `set -e` behavior. So this is safe.

**No other skips found.** No `@pytest.mark.skip` or `pytest.importorskip` in any automated test file.

---

## Self-Challenge Results

| Finding | Original | Final | Reasoning |
|---------|----------|-------|-----------|
| S1-001 | S1 | S1 | The `"raw" in result` assertion is genuinely loose. The companion OSPF test (`test_valid_device_ios`) correctly asserts `"FULL" in result["raw"]`, proving the pattern is known but was missed here. Confirmed ghost for the payload assertion. |
| S1-002 | S1 | S1 | The adversarial test's only assertion (`"error" in result`) cannot distinguish intended behavior from accidental errors. Even a `TypeError` or `AttributeError` propagating up would produce a different error path that still passes the test. Confirmed. |
| S2-001 (autouse) | S2 | Observation | The autouse is necessary for test isolation and is harmless. Downgraded. |
| S2-003 (vault mock chain) | S2 | S2 (low) | The fragility is real but unlikely to manifest with the stable `hvac` library. Kept as S2 with low severity caveat. |
| S3-001 through S3-007 | S3 | S3 | All confirmed via mutation thinking. Each gap allows a specific class of bug to go undetected. |
| S4-001 through S4-007 | S4 | S4 | All confirmed as minor quality issues with no coverage impact. |

---

## Additional Observations (not graded)

1. **`pytest.ini` minimal config:** Only `asyncio_mode = auto` is set. No markers are registered (e.g., `live`), no test paths configured, no warning filters. The `--live` flag used by `run_tests.sh` is not a pytest marker — it's passed as `extra_args` to the pytest command. Live tests don't appear to use `@pytest.mark.live`; they're simply in a separate directory.

2. **Test count per file:** test_input_models (15), test_platform_map (14), test_tools (12), test_transport (5), test_vault (5), test_ingest (8), test_netbox (12), test_ssh (8), test_mcp_server (2), test_rag_pipeline (10). Total: 91 test functions (including parametrized expansions).

3. **Async test support:** All async tests use bare `async def` with `asyncio_mode = auto` in pytest.ini. This is correct for pytest-asyncio and works consistently across both CI and local execution.

4. **`test_tools.py` mock-leakage observation:** In `TestGetOspf::test_valid_device_ios`, `execute_ssh` is mocked to return `"Neighbor ID  State\n1.1.1.1  FULL"`. The test asserts `"FULL" in result["raw"]`. Since `get_ospf()` calls `execute_command()` which calls `execute_ssh()`, and `execute_command()` puts the raw output into `result["raw"]`, the mock's return value flows directly into the assertion. However, this is NOT a ghost pass because: (a) the test also asserts `result["cli_style"] == "ios"` which comes from the inventory lookup (real logic), and (b) `result["_command"]` containing `"show ip ospf neighbor"` verifies that `get_action()` resolved the correct command (real logic). The mock leakage is partial — the `"raw"` assertion is testing the mock, but the other assertions test real code. This is a reasonable trade-off for integration-style tests.
