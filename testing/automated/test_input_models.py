"""UT-001: Input model — custom JSON string validator."""
import pytest
from pydantic import ValidationError

from input_models.models import OspfQuery


class TestJsonStringParsing:
    def test_json_string_parsing(self):
        q = OspfQuery.model_validate('{"device": "R1", "query": "neighbors"}')
        assert q.device == "R1"
        assert q.query == "neighbors"

    def test_malformed_json_rejected(self):
        with pytest.raises(ValidationError):
            OspfQuery.model_validate("not json at all")
