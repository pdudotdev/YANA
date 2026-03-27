# Ghost Pass Detection Checklist — netKB

A ghost pass is a test that always passes regardless of whether the function under test works correctly. It provides false confidence and is worse than no test.

---

## 6-Question Checklist

Apply to every **Category A test** (uses mocks, patches, monkeypatch, or tests error/exception paths).

### Q1 — No-op test
Mentally replace the function-under-test with `pass` (returns `None`).
Would this test still pass?

If yes: the test is not testing the function's behavior — it is testing mock behavior or making a trivially true assertion.

### Q2 — Assertion target
Does the assertion verify the **result of the function**, or does it verify that **a mock was called**?

```python
# Ghost pass: asserting mock was called, not that result is correct
mock_get_secret.assert_called_once_with("netkb/router", "password")  ← tests nothing about behavior

# Real test: asserting actual result
assert result == {"username": "admin", "password": "secret"}
```

### Q3 — Assertion specificity
Is the assertion exact, or is it loose?

```python
# Loose (ghost pass risk)
assert result is not None
assert "error" in result
assert isinstance(result, dict)

# Exact (real test)
assert result == {"error": "Device 'R99' not found in inventory"}
assert result["status"] == "FULL"
assert len(result["neighbors"]) == 3
```

### Q4 — Mock leakage
Does the mock's return value flow **directly** into the assertion, without the function-under-test transforming it?

```python
# Ghost pass: mock returns exactly what assertion checks
mock_execute_ssh.return_value = {"output": "Neighbor 10.0.0.1 is FULL"}
# ... test calls get_ospf() ...
assert result["output"] == "Neighbor 10.0.0.1 is FULL"  ← mock gave the answer
```

The function-under-test could be completely broken and this test would still pass, because the assertion checks the mock's return value, not the function's logic.

### Q5 — Exception specificity
For `pytest.raises` tests: is the exception type specific?

```python
# Loose (ghost pass risk) — catches any exception, even a typo or import error
with pytest.raises(Exception):
    get_ospf(device="unknown", query="neighbors")

# Specific (real test)
with pytest.raises(KeyError):
    ...
# Or better — check the error response shape:
result = get_ospf(device="unknown", query="neighbors")
assert result == {"error": "Device 'unknown' not found in inventory"}
```

### Q6 — Error content
For error-dict tests: does the assertion check the error **message content**, or just that an error key exists?

```python
# Shallow (ghost pass risk)
assert "error" in result
assert result.get("error") is not None

# Real test
assert result["error"] == "Device 'R99' not found in inventory"
# or at minimum:
assert "R99" in result["error"]
assert "not found" in result["error"]
```

---

## Common Ghost Pass Patterns

### Pattern 1: Mock gives the answer
```python
mock_func.return_value = {"status": "ok", "neighbors": 3}
result = function_under_test(...)
assert result["status"] == "ok"       # ← mock gave this value
assert result["neighbors"] == 3       # ← mock gave this value too
```
The function could `return None` and the test would fail. But the function could also `return mock_func.return_value` directly and the test would still pass, hiding any real logic bugs.

**Detection:** Can you remove the entire body of `function_under_test` and replace with `return mock_func.return_value`? If the test still passes, it's a ghost.

### Pattern 2: No assertion at all
```python
def test_something():
    result = function_under_test(...)
    # No assert statement
```
Always passes. Usually a test skeleton that was never completed.

### Pattern 3: Assert on mock object state
```python
mock_execute.assert_called_once()         # ← verifies function was called
mock_execute.assert_called_with("show ip ospf neighbors")  # ← verifies arguments
```
These verify that the function-under-test called the mock correctly, but say nothing about what the function-under-test did with the mock's return value.

### Pattern 4: Overly broad exception catch
```python
with pytest.raises(Exception):
    function_under_test(bad_input)
```
Passes even if the wrong exception is raised (e.g., an `ImportError` or `AttributeError` unrelated to the test scenario).

### Pattern 5: Parametrize with a single case
```python
@pytest.mark.parametrize("vendor", ["cisco_ios"])
def test_vendor_filter(vendor):
    ...
```
Looks like parametrized coverage but tests exactly one case. No different from a non-parametrized test.

### Pattern 6: Fixture provides the expected value
```python
def test_get_ospf(mock_inventory):
    # mock_inventory patches devices with MOCK_DEVICES
    result = get_ospf(device="R1", query="neighbors")
    assert result["device"] == "R1"  ← MOCK_DEVICES["R1"] has this key
```
If `get_ospf` simply passes through device info from the inventory dict without transformation, this test only verifies that MOCK_DEVICES has the right structure, not that `get_ospf` does anything useful.

---

## Quick Assertion Check (Category B tests only)

For simple construction/validation tests (no mocks), ask only:
1. Is the assertion specific enough that a wrong value would fail it?
2. Could the assertion pass with a completely different return value?

```python
# Passes with any non-empty string — too loose
assert result.vrf != ""

# Passes only with the exact expected value — real test
assert result.vrf == "VRF1"
```
