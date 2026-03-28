"""RAG tool: search the OSPF knowledge base."""
import logging
from pathlib import Path

from input_models.models import KBQuery

_CHROMA_DIR = str(Path(__file__).resolve().parent.parent / "data" / "chroma")
_COLLECTION = "ospf_kb"
_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

log = logging.getLogger("netkb.rag")

# Lazy-initialized at first call so a ChromaDB failure does not prevent
# the device tools (get_ospf, get_interfaces) from loading.
_embeddings = None
_vectorstore = None


def _get_vectorstore():
    global _embeddings, _vectorstore
    if _vectorstore is None:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import Chroma
        _embeddings = HuggingFaceEmbeddings(model_name=_EMBEDDING_MODEL)
        _vectorstore = Chroma(
            persist_directory=_CHROMA_DIR,
            embedding_function=_embeddings,
            collection_name=_COLLECTION,
        )
    return _vectorstore


async def search_knowledge_base(params: KBQuery) -> dict:
    """Search the OSPF knowledge base for relevant documentation.

    Returns ranked document chunks matching the query. Use the optional
    vendor and topic filters to narrow results:
    - vendor: cisco_ios, arista_eos, juniper_junos, aruba_aoscx, mikrotik_ros
    - topic: rfc, vendor_guide
    """
    where = {}
    if params.vendor:
        where["vendor"] = params.vendor
    if params.topic:
        where["topic"] = params.topic

    # ChromaDB requires $and for compound filters
    if len(where) > 1:
        where = {"$and": [{k: v} for k, v in where.items()]}

    search_kwargs = {"k": params.top_k}
    if where:
        search_kwargs["filter"] = where

    try:
        vs = _get_vectorstore()
        results = vs.similarity_search(params.query, **search_kwargs)
    except Exception as exc:
        log.error("Knowledge base search failed: %s", exc)
        return {"error": f"Knowledge base unavailable: {exc}"}

    return {
        "results": [
            {"content": doc.page_content, "metadata": doc.metadata}
            for doc in results
        ]
    }
