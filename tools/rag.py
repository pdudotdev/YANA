"""RAG tool: search the network knowledge base."""
import asyncio
import logging

from input_models.models import KBQuery
from tools import CHROMA_DIR

_CHROMA_DIR = str(CHROMA_DIR)
_COLLECTION = "network_kb"
_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

log = logging.getLogger("yana.rag")

# Lazy-initialized at first call so a ChromaDB failure does not prevent
# the device tools (get_ospf, get_interfaces) from loading.
_embeddings = None
_vectorstore = None


def _get_vectorstore():
    global _embeddings, _vectorstore
    if _vectorstore is None:
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_chroma import Chroma
        _embeddings = HuggingFaceEmbeddings(model_name=_EMBEDDING_MODEL)
        _vectorstore = Chroma(
            persist_directory=_CHROMA_DIR,
            embedding_function=_embeddings,
            collection_name=_COLLECTION,
        )
    return _vectorstore


async def search_knowledge_base(params: KBQuery) -> dict:
    """Search the network knowledge base for relevant documentation.

    Returns ranked document chunks matching the query. Use the optional
    filters to narrow results:
    - vendor: cisco_ios, arista_eos, juniper_junos, aruba_aoscx, mikrotik_ros
    - topic: rfc, vendor_guide
    - protocol: ospf, bgp, eigrp
    """
    where = {}
    if params.vendor:
        where["vendor"] = params.vendor
    if params.topic:
        where["topic"] = params.topic
    if params.protocol:
        where["protocol"] = params.protocol

    # ChromaDB requires $and for compound filters
    if len(where) > 1:
        where = {"$and": [{k: v} for k, v in where.items()]}

    search_kwargs = {"k": params.top_k}
    if where:
        search_kwargs["filter"] = where

    def _sync_search():
        vs = _get_vectorstore()
        return vs.similarity_search(params.query, **search_kwargs)

    try:
        results = await asyncio.to_thread(_sync_search)
    except Exception as exc:
        log.error("Knowledge base search failed: %s", exc)
        return {"error": f"Knowledge base unavailable: {exc}"}

    return {
        "results": [
            {"content": doc.page_content, "metadata": doc.metadata}
            for doc in results
        ]
    }
