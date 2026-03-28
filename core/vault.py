"""HashiCorp Vault client — reads secrets from KV v2 with env var fallback."""
import logging
import os

log = logging.getLogger("netkb.vault")

_VAULT_FAILED = object()
_cache: dict[str, object] = {}
_sources: dict[str, str] = {}


def get_secret(path: str, key: str, fallback_env: str = "", quiet: bool = False) -> str | None:
    """Read a secret from Vault KV v2, falling back to an env var."""
    vault_addr = os.getenv("VAULT_ADDR", "").strip()
    vault_token = os.getenv("VAULT_TOKEN", "").strip()

    if not vault_addr or not vault_token:
        _sources[path] = "env"
        return os.getenv(fallback_env) if fallback_env else None

    if path in _cache:
        cached = _cache[path]
        if cached is _VAULT_FAILED or key not in cached:
            return os.getenv(fallback_env) if fallback_env else None
        return cached[key]

    try:
        import hvac
        client = hvac.Client(url=vault_addr, token=vault_token)
        client.session.timeout = (5, 10)
        response = client.secrets.kv.v2.read_secret_version(
            path=path, mount_point="secret", raise_on_deleted_version=True
        )
        data: dict = response["data"]["data"]
        _cache[path] = data
        _sources[path] = "vault"
        log_fn = log.debug if quiet else log.info
        log_fn("Vault: loaded secret path '%s'", path)
        return data.get(key) or (os.getenv(fallback_env) if fallback_env else None)
    except Exception as exc:
        log_fn = log.debug if quiet else log.warning
        log_fn("Vault unavailable (path=%s): %s — falling back to env var", path, exc)
        _cache[path] = _VAULT_FAILED
        _sources[path] = "env"
        return os.getenv(fallback_env) if fallback_env else None


def get_source(path: str) -> str:
    """Return which backend provided the secret at the given path."""
    return _sources.get(path, "unknown")
