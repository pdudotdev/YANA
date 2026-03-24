"""IT-001: RAG pipeline integration — requires populated ChromaDB."""
import asyncio
from pathlib import Path

import pytest

CHROMA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "chroma"

pytestmark = pytest.mark.skipif(
    not CHROMA_DIR.exists(),
    reason="ChromaDB not populated — run 'python ingest.py' first",
)


@pytest.fixture(scope="module")
def search():
    """Import search_knowledge_base (loads ChromaDB at import time)."""
    from tools.rag import search_knowledge_base
    return search_knowledge_base


@pytest.fixture(scope="module")
def run(search):
    """Helper to run async search synchronously."""
    def _run(query, **kwargs):
        from input_models.models import KBQuery
        params = KBQuery(query=query, **kwargs)
        return asyncio.get_event_loop().run_until_complete(search(params))
    return _run


class TestSearchReturnsResults:
    def test_basic_query(self, run):
        result = run("OSPF neighbor states")
        assert len(result["results"]) > 0

    def test_results_have_metadata(self, run):
        result = run("OSPF timers")
        for r in result["results"]:
            assert "content" in r
            assert "metadata" in r
            assert "source" in r["metadata"]
            assert "vendor" in r["metadata"]
            assert "topic" in r["metadata"]


class TestFiltering:
    def test_vendor_filter(self, run):
        result = run("OSPF configuration", vendor="cisco_ios")
        for r in result["results"]:
            assert r["metadata"]["vendor"] == "cisco_ios"

    def test_topic_filter(self, run):
        result = run("OSPF neighbor state machine", topic="rfc")
        for r in result["results"]:
            assert r["metadata"]["topic"] == "rfc"

    def test_compound_filter(self, run):
        """Both vendor + topic should work without ChromaDB $and error."""
        result = run("OSPF configuration", vendor="cisco_ios", topic="vendor_guide")
        for r in result["results"]:
            assert r["metadata"]["vendor"] == "cisco_ios"
            assert r["metadata"]["topic"] == "vendor_guide"

    def test_intent_topic(self, run):
        result = run("Which devices are ABRs", topic="intent")
        assert len(result["results"]) > 0
        for r in result["results"]:
            assert r["metadata"]["topic"] == "intent"


class TestTopK:
    def test_top_k_limits_results(self, run):
        result = run("OSPF", top_k=2)
        assert len(result["results"]) == 2

    def test_default_top_k(self, run):
        result = run("OSPF")
        assert len(result["results"]) == 5
