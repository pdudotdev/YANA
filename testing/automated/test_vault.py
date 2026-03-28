"""UT-005: Vault client — cache, fallback, sentinel behavior."""
from unittest.mock import MagicMock, patch



class TestVault:
    def setup_method(self):
        """Reset vault cache and sources before each test."""
        import core.vault
        core.vault._cache.clear()
        core.vault._sources.clear()

    def test_no_vault_env_falls_back(self, monkeypatch):
        """Without VAULT_ADDR, returns the fallback env var."""
        monkeypatch.delenv("VAULT_ADDR", raising=False)
        monkeypatch.delenv("VAULT_TOKEN", raising=False)
        monkeypatch.setenv("MY_SECRET", "from_env")

        from core.vault import get_secret
        result = get_secret("some/path", "key", fallback_env="MY_SECRET")
        assert result == "from_env"

    def test_no_vault_no_fallback_returns_none(self, monkeypatch):
        """Without VAULT_ADDR and no fallback env, returns None."""
        monkeypatch.delenv("VAULT_ADDR", raising=False)
        monkeypatch.delenv("VAULT_TOKEN", raising=False)

        from core.vault import get_secret
        result = get_secret("some/path", "key")
        assert result is None

    def test_cache_hit(self, monkeypatch):
        """Cached values are returned without calling Vault again."""
        monkeypatch.setenv("VAULT_ADDR", "http://fake:8200")
        monkeypatch.setenv("VAULT_TOKEN", "fake-token")

        import core.vault
        core.vault._cache["test/path"] = {"username": "admin"}

        result = core.vault.get_secret("test/path", "username")
        assert result == "admin"

    def test_cache_missing_key_falls_back(self, monkeypatch):
        """Cached path but missing key falls back to env var."""
        monkeypatch.setenv("VAULT_ADDR", "http://fake:8200")
        monkeypatch.setenv("VAULT_TOKEN", "fake-token")
        monkeypatch.setenv("FALLBACK", "env_value")

        import core.vault
        core.vault._cache["test/path"] = {"username": "admin"}

        result = core.vault.get_secret("test/path", "nonexistent", fallback_env="FALLBACK")
        assert result == "env_value"
        assert "test/path" not in core.vault._sources

    def test_vault_failure_sets_sentinel(self, monkeypatch):
        """Failed Vault call caches _VAULT_FAILED and falls back."""
        monkeypatch.setenv("VAULT_ADDR", "http://fake:8200")
        monkeypatch.setenv("VAULT_TOKEN", "fake-token")
        monkeypatch.setenv("FALLBACK", "env_value")

        import core.vault
        # Simulate Vault import + failure
        with patch.dict("sys.modules", {"hvac": MagicMock()}):
            import hvac
            hvac.Client.return_value.secrets.kv.v2.read_secret_version.side_effect = Exception("unreachable")

            result = core.vault.get_secret("fail/path", "key", fallback_env="FALLBACK")
            assert result == "env_value"
            assert core.vault._cache["fail/path"] is core.vault._VAULT_FAILED


class TestVaultSourceTracking:
    def setup_method(self):
        import core.vault
        core.vault._cache.clear()
        core.vault._sources.clear()

    def test_no_vault_env_sets_source_env(self, monkeypatch):
        """Without Vault config, source is recorded as 'env'."""
        monkeypatch.delenv("VAULT_ADDR", raising=False)
        monkeypatch.delenv("VAULT_TOKEN", raising=False)

        import core.vault
        core.vault.get_secret("some/path", "key", fallback_env="MISSING_VAR")
        assert core.vault.get_source("some/path") == "env"

    def test_vault_success_sets_source_vault(self, monkeypatch):
        """Successful Vault read records source as 'vault'."""
        monkeypatch.setenv("VAULT_ADDR", "http://fake:8200")
        monkeypatch.setenv("VAULT_TOKEN", "fake-token")

        import core.vault
        mock_response = {"data": {"data": {"username": "admin"}}}
        with patch.dict("sys.modules", {"hvac": MagicMock()}):
            import hvac
            hvac.Client.return_value.secrets.kv.v2.read_secret_version.return_value = mock_response

            core.vault.get_secret("yana/router", "username")
            assert core.vault.get_source("yana/router") == "vault"

    def test_vault_failure_sets_source_env(self, monkeypatch):
        """Failed Vault read falls back and records source as 'env'."""
        monkeypatch.setenv("VAULT_ADDR", "http://fake:8200")
        monkeypatch.setenv("VAULT_TOKEN", "fake-token")

        import core.vault
        with patch.dict("sys.modules", {"hvac": MagicMock()}):
            import hvac
            hvac.Client.return_value.secrets.kv.v2.read_secret_version.side_effect = Exception("unreachable")

            core.vault.get_secret("yana/router", "username")
            assert core.vault.get_source("yana/router") == "env"

    def test_get_source_unknown_path(self):
        """Unqueried path returns 'unknown'."""
        import core.vault
        assert core.vault.get_source("never/queried") == "unknown"
