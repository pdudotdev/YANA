# Async Safety Checklist — netKB

Use this during Phase 3. For each item, determine PASS, FAIL, or N/A based on the code you read in Phase 2.

---

## Import-Time Blocking

These modules execute code at import time. Verify each one:

| Module | Import-time action | Blocks event loop? | Verdict |
|--------|--------------------|--------------------|---------|
| `core/settings.py` | Calls `get_secret()` (Vault HTTP) and `os.getenv()` | Vault HTTP is blocking — acceptable only if this runs before the event loop starts | Check FastMCP startup order |
| `core/inventory.py` | Calls `load_devices()` (NetBox HTTP via pynetbox) | Blocking synchronous HTTP — acceptable only if before event loop starts | Check import chain from `server/MCPServer.py` |
| `tools/rag.py` | Defines constants only (`_CHROMA_DIR`, `_COLLECTION`, `_MODEL`) | No — lazy init is correct | PASS expected |
| `server/MCPServer.py` | Imports all of the above transitively | Transitive — all blocking I/O happens here before `mcp.run()` | Key question: does `mcp.run()` start the event loop? If yes, all import-time calls precede the loop — acceptable. |

**Key principle:** FastMCP's `mcp.run()` starts the asyncio event loop. All module-level code runs at import time, which is before `mcp.run()`. Import-time blocking is acceptable for a startup-once server but would be a problem if modules were hot-reloaded or if `mcp.run()` is called inside an already-running event loop.

---

## Semaphore Safety

| Check | Location | Expected | Verify |
|-------|----------|----------|--------|
| Semaphore created at module level | `transport/__init__.py`, line ~11 | `asyncio.Semaphore(SSH_MAX_CONCURRENT)` | In Python ≥ 3.10, Semaphore does NOT require a running loop at creation. Verify Python version requirement. |
| Semaphore used via `async with` | `transport/__init__.py` | `async with _cmd_sem:` — guarantees release on exception | Check: no manual `.acquire()` / `.release()` calls anywhere |
| Timeout on semaphore acquisition | `transport/__init__.py` | Currently NONE — `async with _cmd_sem` blocks indefinitely | If all 5 slots are occupied by stalled connections, new requests wait forever. Report as S1 or S2 depending on realism of trigger. |
| Slot held during retry sleep | `transport/ssh.py` | `asyncio.sleep(SSH_RETRY_DELAY)` inside the semaphore context | A retrying connection holds its slot during sleep, reducing effective concurrency from 5 to (5 - retrying_count) |

---

## Lazy Initialization Race

| Pattern | Location | Risk assessment |
|---------|----------|-----------------|
| `_get_vectorstore()` global mutation | `tools/rag.py` | The function checks `if _vectorstore is None` then initializes. In CPython's cooperative async model, a race requires an `await` between the None check and the assignment. Inspect the function body: if there is no `await` in the initialization path, CPython's GIL prevents the race. If there IS an `await` (e.g., `await some_async_call()`), two concurrent coroutines can both enter the branch. |

---

## Connection Cleanup

| Check | Location | Expected |
|-------|----------|----------|
| SSH connection uses `async with` | `transport/ssh.py` | `async with _build_cli(device, timeout_ops) as conn:` — guarantees `__aexit__` on normal exit AND on exception |
| Connection re-created per retry | `transport/ssh.py` | `_build_cli()` called inside the for loop — each retry attempt opens a fresh connection |
| `OpenException` bypasses retry | `transport/ssh.py` | `OpenException` is re-raised immediately (correct — auth failures should not retry). Verify it still propagates cleanly through `execute_command`. |
| Timeout behavior inside session | `transport/ssh.py` | If `send_input_async` times out, what exception is raised? Does scrapli's `async with` ensure cleanup? |
