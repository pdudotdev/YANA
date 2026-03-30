"""UT-014: query_intent tool."""
from unittest.mock import patch

from input_models.models import IntentQuery
from tools.intent import query_intent

_SAMPLE_INTENT = {
    "autonomous_systems": {"AS1010": {"name": "Enterprise"}},
    "routers": {
        "R1": {"roles": ["ABR"], "igp": {"area": "0.0.0.0"}},
        "R2": {"roles": ["ASBR"], "igp": {"area": "0.0.0.1"}},
    },
}


class TestQueryIntent:
    async def test_all_devices_returned_when_no_filter(self, tmp_path):
        import json
        intent_file = tmp_path / "INTENT.json"
        intent_file.write_text(json.dumps(_SAMPLE_INTENT))

        with patch("tools.intent._INTENT_JSON", intent_file):
            result = await query_intent(IntentQuery())
        assert "routers" in result
        assert set(result["routers"].keys()) == {"R1", "R2"}

    async def test_single_device_filter(self, tmp_path):
        import json
        intent_file = tmp_path / "INTENT.json"
        intent_file.write_text(json.dumps(_SAMPLE_INTENT))

        with patch("tools.intent._INTENT_JSON", intent_file):
            result = await query_intent(IntentQuery(device="R1"))
        assert result["device"] == "R1"
        assert result["intent"]["roles"] == ["ABR"]

    async def test_unknown_device_error(self, tmp_path):
        import json
        intent_file = tmp_path / "INTENT.json"
        intent_file.write_text(json.dumps(_SAMPLE_INTENT))

        with patch("tools.intent._INTENT_JSON", intent_file):
            result = await query_intent(IntentQuery(device="NONEXISTENT"))
        assert "error" in result
        assert "Unknown device" in result["error"]
        assert "R1" in result["error"]

    async def test_missing_json_returns_error(self, tmp_path):
        """When INTENT.json does not exist, return error."""
        missing = tmp_path / "MISSING.json"

        with patch("tools.intent._INTENT_JSON", missing):
            result = await query_intent(IntentQuery())
        assert "error" in result
