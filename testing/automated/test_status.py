"""UT-012: get_status tool."""
from unittest.mock import patch

from tools.status import get_status


class TestGetStatus:
    async def test_structure(self):
        """Result must have all four expected keys."""
        with patch("tools.status.load_intent", return_value=None), \
             patch("tools.status._CHROMA_DIR") as mock_chroma:
            mock_chroma.exists.return_value = False
            result = await get_status()
        assert set(result.keys()) == {"inventory", "vault", "intent", "chromadb"}

    async def test_inventory_empty(self, monkeypatch):
        import core.inventory
        monkeypatch.setattr(core.inventory, "devices", {})
        monkeypatch.setattr(core.inventory, "source", "empty")

        with patch("tools.status.load_intent", return_value=None), \
             patch("tools.status._CHROMA_DIR") as mock_chroma:
            mock_chroma.exists.return_value = False
            result = await get_status()
        assert result["inventory"]["source"] == "empty"
        assert result["inventory"]["device_count"] == 0

    async def test_inventory_loaded(self, monkeypatch):
        import core.inventory
        monkeypatch.setattr(core.inventory, "devices", {"R1": {}, "R2": {}})
        monkeypatch.setattr(core.inventory, "source", "netbox")

        with patch("tools.status.load_intent", return_value=None), \
             patch("tools.status._CHROMA_DIR") as mock_chroma:
            mock_chroma.exists.return_value = False
            result = await get_status()
        assert result["inventory"]["source"] == "netbox"
        assert result["inventory"]["device_count"] == 2

    async def test_inventory_network_json_fallback(self, monkeypatch):
        import core.inventory
        monkeypatch.setattr(core.inventory, "devices", {"R1": {}})
        monkeypatch.setattr(core.inventory, "source", "network_json")

        with patch("tools.status.load_intent", return_value=None), \
             patch("tools.status._CHROMA_DIR") as mock_chroma:
            mock_chroma.exists.return_value = False
            result = await get_status()
        assert result["inventory"]["source"] == "network_json"

    async def test_vault_source_reported(self, monkeypatch):
        import core.vault
        monkeypatch.delenv("VAULT_ADDR", raising=False)
        monkeypatch.delenv("VAULT_TOKEN", raising=False)
        core.vault._cache.clear()
        core.vault._sources.clear()

        with patch("tools.status.load_intent", return_value=None), \
             patch("tools.status._CHROMA_DIR") as mock_chroma:
            mock_chroma.exists.return_value = False
            result = await get_status()
        assert result["vault"]["source"] in ("vault", "env", "unknown")

    async def test_intent_netbox(self):
        sample_intent = {"routers": {"R1": {}, "R2": {}}}
        with patch("tools.status.load_intent", return_value=sample_intent), \
             patch("tools.status._CHROMA_DIR") as mock_chroma:
            mock_chroma.exists.return_value = False
            result = await get_status()
        assert result["intent"]["source"] == "netbox"
        assert result["intent"]["router_count"] == 2

    async def test_intent_json_fallback(self, tmp_path):
        intent_file = tmp_path / "INTENT.json"
        intent_file.write_text('{"routers": {}}')

        with patch("tools.status.load_intent", return_value=None), \
             patch("tools.status._INTENT_JSON", intent_file), \
             patch("tools.status._CHROMA_DIR") as mock_chroma:
            mock_chroma.exists.return_value = False
            result = await get_status()
        assert result["intent"]["source"] == "intent_json"

    async def test_chromadb_available(self, tmp_path):
        (tmp_path / "somefile").write_text("data")

        with patch("tools.status.load_intent", return_value=None), \
             patch("tools.status._CHROMA_DIR", tmp_path):
            result = await get_status()
        assert result["chromadb"]["available"] is True

    async def test_chromadb_unavailable(self, tmp_path):
        with patch("tools.status.load_intent", return_value=None), \
             patch("tools.status._CHROMA_DIR") as mock_chroma:
            mock_chroma.exists.return_value = False
            result = await get_status()
        assert result["chromadb"]["available"] is False
