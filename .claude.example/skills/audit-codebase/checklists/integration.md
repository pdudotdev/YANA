# Integration Point Checklist — netKB

Use this during Phase 6. For each integration point, verify the listed behaviors against the code you read in Phase 2.

---

## Vault (`core/vault.py`)

| Check | What to verify |
|-------|----------------|
| `_VAULT_FAILED` sentinel is cached permanently | Once set, does any code path ever clear it or retry? Is there a TTL? A manual reset? If Vault recovers after being down at startup, can the server pick up secrets without a restart? |
| Env var fallback | When `_VAULT_FAILED` is set, does `get_secret()` correctly fall back to `fallback_env` via `os.getenv()`? |
| `hvac` import is inside the function | This means a missing `hvac` package produces a runtime `ModuleNotFoundError` on first call, not an import error at startup. Is this the intended behavior? |
| Vault session timeout | `client.session.timeout = (5, 10)` — connect 5s, read 10s. Verify the timeout is actually set before the first request. |
| Cache key structure | Cache key is `path`, value is the full secret `data` dict. A second call for a different `key` on the same `path` should hit the cache and slice the dict. Verify this is correct. |

---

## NetBox (`core/netbox.py`, `core/inventory.py`)

| Check | What to verify |
|-------|----------------|
| Import-time `load_devices()` call | `core/inventory.py` calls `load_devices()` at module level. If NetBox is unreachable, what exception propagates? Does it crash the server import chain or get caught? |
| Missing `primary_ip` | Does `load_devices()` skip devices with `primary_ip=None`? Verify the check is present and the device is excluded without crashing. |
| Missing `platform` or `cli_style` | Does `load_devices()` skip devices with missing custom fields? Is a warning logged? |
| `load_intent()` prefix fallback | Does it try `netkb-` prefix first, then fall back to `dblcheck-`? Verify both code paths exist. |
| NetBox session timeout | `(5, 15)` — verify it's applied to the pynetbox session object before requests. |
| Empty NetBox result | If `load_devices()` returns an empty dict (no devices in NetBox), does the server start with empty inventory and return clean errors on unknown device queries? |

---

## ChromaDB (`tools/rag.py`)

| Check | What to verify |
|-------|----------------|
| Lazy initialization | `_get_vectorstore()` is only called on the first `search_knowledge_base` invocation. Verify no initialization happens at import time. |
| Missing `_CHROMA_DIR` | What does ChromaDB's `PersistentClient` do if the directory doesn't exist — create it, raise, or return an empty store? Verify the code handles the failure case. |
| HuggingFace model download | `HuggingFaceEmbeddings(model_name=...)` downloads the model on first load if not cached. Is this failure handled? |
| Empty `where` filter | If neither `vendor` nor `topic` is provided in `KBQuery`, is an empty `where = {}` dict avoided before calling `similarity_search`? An empty `where` may be rejected by ChromaDB. |
| Error response shape | If `_get_vectorstore()` or `similarity_search` raises, is the exception caught and returned as `{"error": ...}`? |

---

## Scrapli SSH (`transport/ssh.py`)

| Check | What to verify |
|-------|----------------|
| Custom definition files | `mikrotik_routeros.yaml` and `vyos_vyos.yaml` in `platforms/definitions/`. Are they loaded at startup or on first use? If a file is malformed, when does the error surface? |
| Per-connection credential lookup | `get_secret()` is called in `_build_cli()` for every SSH connection. Since Vault results are cached, only the first connection to each cli_style pays the HTTP cost. Verify this is correct. |
| MikroTik `+ct` suffix | Is `f"{username}+ct"` applied for MikroTik connections specifically, and NOT for other platforms? |
| VyOS transport | Does VyOS use a different scrapli transport class (`Ssh2Options` or `TransportSsh2Options`) compared to other platforms? Is this set correctly in `_build_cli()`? |
| Credential path per cli_style | Is the Vault path per cli_style (`netkb/router{cli_style}`) correct for all platforms, or does it use a shared path? |
