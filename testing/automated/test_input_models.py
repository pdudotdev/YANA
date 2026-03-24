"""UT-001: Input model validation."""
import pytest
from pydantic import ValidationError

from input_models.models import InterfacesQuery, KBQuery, OspfQuery


class TestOspfQuery:
    @pytest.mark.parametrize("query", ["neighbors", "database", "borders", "config", "interfaces", "details"])
    def test_valid_query_types(self, query):
        q = OspfQuery(device="R1", query=query)
        assert q.query == query

    def test_invalid_query_rejected(self):
        with pytest.raises(ValidationError):
            OspfQuery(device="R1", query="invalid")

    def test_vrf_valid(self):
        q = OspfQuery(device="R1", query="neighbors", vrf="VRF1")
        assert q.vrf == "VRF1"

    @pytest.mark.parametrize("bad_vrf", [
        "VRF;drop",       # semicolon injection
        "VRF|grep",       # pipe injection
        "VRF 1",          # space
        "a" * 33,         # too long
        "",               # empty string
    ])
    def test_vrf_injection_rejected(self, bad_vrf):
        with pytest.raises(ValidationError):
            OspfQuery(device="R1", query="neighbors", vrf=bad_vrf)

    def test_json_string_parsing(self):
        q = OspfQuery.model_validate('{"device": "R1", "query": "neighbors"}')
        assert q.device == "R1"
        assert q.query == "neighbors"

    def test_malformed_json_rejected(self):
        with pytest.raises(ValidationError):
            OspfQuery.model_validate("not json at all")


class TestInterfacesQuery:
    def test_valid(self):
        q = InterfacesQuery(device="R1")
        assert q.device == "R1"


class TestKBQuery:
    def test_valid_full(self):
        q = KBQuery(query="OSPF timers", vendor="cisco_ios", topic="rfc", top_k=3)
        assert q.vendor == "cisco_ios"
        assert q.topic == "rfc"
        assert q.top_k == 3

    def test_valid_minimal(self):
        q = KBQuery(query="OSPF")
        assert q.vendor is None
        assert q.topic is None
        assert q.top_k == 5

    def test_invalid_vendor_rejected(self):
        with pytest.raises(ValidationError):
            KBQuery(query="test", vendor="invalid_vendor")

    def test_invalid_topic_rejected(self):
        with pytest.raises(ValidationError):
            KBQuery(query="test", topic="bad_topic")

    def test_top_k_too_high(self):
        with pytest.raises(ValidationError):
            KBQuery(query="test", top_k=11)

    def test_top_k_too_low(self):
        with pytest.raises(ValidationError):
            KBQuery(query="test", top_k=0)

    def test_query_too_long(self):
        with pytest.raises(ValidationError):
            KBQuery(query="x" * 501)

    def test_query_at_max_length(self):
        q = KBQuery(query="x" * 500)
        assert len(q.query) == 500
