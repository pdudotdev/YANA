"""RAG tool: search the OSPF knowledge base."""
from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from input_models.models import KBQuery

_CHROMA_DIR = str(Path(__file__).resolve().parent.parent / "data" / "chroma")
_COLLECTION = "ospf_kb"

# Load once at module level
_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
_vectorstore = Chroma(
    persist_directory=_CHROMA_DIR,
    embedding_function=_embeddings,
    collection_name=_COLLECTION,
)


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

    results = _vectorstore.similarity_search(params.query, **search_kwargs)

    return {
        "results": [
            {"content": doc.page_content, "metadata": doc.metadata}
            for doc in results
        ]
    }
