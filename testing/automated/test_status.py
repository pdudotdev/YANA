"""UT-012: get_status tool."""
from unittest.mock import patch

from tools.status import get_status


class TestGetStatus:
    async def test_structure(self):
        """Result must have all three expected keys."""
        with patch("tools.status._CHROMA_DIR") as mock_chroma, \
             patch("tools.status._INTENT_JSON") as mock_intent:
            mock_chroma.exists.return_value = False
            mock_intent.exists.return_value = False
            result = await get_status()
        assert set(result.keys()) == {"inventory", "intent", "chromadb"}

    async def test_inventory_loaded(self, monkeypatch):
        import core.inventory
        monkeypatch.setattr(core.inventory, "devices", {"R1": {}, "R2": {}})
        monkeypatch.setattr(core.inventory, "source", "network_json")

        with patch("tools.status._CHROMA_DIR") as mock_chroma, \
             patch("tools.status._INTENT_JSON") as mock_intent:
            mock_chroma.exists.return_value = False
            mock_intent.exists.return_value = False
            result = await get_status()
        assert result["inventory"]["source"] == "network_json"
        assert result["inventory"]["device_count"] == 2

    async def test_intent_json_loaded(self, tmp_path):
        intent_file = tmp_path / "INTENT.json"
        intent_file.write_text('{"routers": {"R1": {}, "R2": {}}}')

        with patch("tools.status._INTENT_JSON", intent_file), \
             patch("tools.status._CHROMA_DIR") as mock_chroma:
            mock_chroma.exists.return_value = False
            result = await get_status()
        assert result["intent"]["source"] == "intent_json"
        assert result["intent"]["router_count"] == 2

    async def test_intent_unavailable(self, tmp_path):
        missing = tmp_path / "MISSING.json"

        with patch("tools.status._INTENT_JSON", missing), \
             patch("tools.status._CHROMA_DIR") as mock_chroma:
            mock_chroma.exists.return_value = False
            result = await get_status()
        assert result["intent"]["source"] == "unavailable"
