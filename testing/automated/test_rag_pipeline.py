"""IT-001: RAG pipeline integration — requires populated ChromaDB."""
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
    """Helper to run async search synchronously — returns a coroutine caller."""
    async def _run(query, **kwargs):
        from input_models.models import KBQuery
        params = KBQuery(query=query, **kwargs)
        return await search(params)
    return _run


class TestSearchReturnsResults:
    async def test_basic_query(self, run):
        result = await run("OSPF neighbor states")
        assert len(result["results"]) > 0

    async def test_results_have_metadata(self, run):
        result = await run("OSPF timers")
        for r in result["results"]:
            assert "content" in r
            assert "metadata" in r
            assert "source" in r["metadata"]
            assert "vendor" in r["metadata"]
            assert "topic" in r["metadata"]


class TestFiltering:
    async def test_vendor_filter(self, run):
        result = await run("OSPF configuration", vendor="cisco_ios")
        assert len(result["results"]) > 0
        for r in result["results"]:
            assert r["metadata"]["vendor"] == "cisco_ios"

    async def test_topic_filter(self, run):
        result = await run("OSPF neighbor state machine", topic="rfc")
        assert len(result["results"]) > 0
        for r in result["results"]:
            assert r["metadata"]["topic"] == "rfc"

    async def test_compound_filter(self, run):
        """Both vendor + topic should work without ChromaDB $and error."""
        result = await run("OSPF configuration", vendor="cisco_ios", topic="vendor_guide")
        assert len(result["results"]) > 0
        for r in result["results"]:
            assert r["metadata"]["vendor"] == "cisco_ios"
            assert r["metadata"]["topic"] == "vendor_guide"


class TestSearchErrorPath:
    async def test_vectorstore_failure_returns_error_dict(self, search):
        """ChromaDB/embedding failure returns structured error dict, not an exception."""
        from unittest.mock import patch
        with patch("tools.rag._get_vectorstore", side_effect=RuntimeError("DB corrupt")):
            from input_models.models import KBQuery
            result = await search(KBQuery(query="OSPF neighbors"))
        assert "error" in result
        assert "results" not in result
        assert "Knowledge base unavailable" in result["error"]


class TestTopK:
    async def test_top_k_limits_results(self, run):
        result = await run("OSPF", top_k=2)
        assert len(result["results"]) == 2

    async def test_default_top_k(self, run):
        result = await run("OSPF")
        assert len(result["results"]) == 5
