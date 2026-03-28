"""Ingest OSPF knowledge base docs into ChromaDB via LangChain."""
import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from tools.rag import _CHROMA_DIR, _COLLECTION, _EMBEDDING_MODEL

DOCS_DIR = Path(__file__).parent / "docs"
CHROMA_DIR = Path(_CHROMA_DIR)
COLLECTION_NAME = _COLLECTION
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100


def extract_metadata(file_path: Path) -> dict:
    """Derive vendor and topic metadata from filename."""
    name = file_path.stem
    if name.startswith("vendor_"):
        vendor = name[len("vendor_"):]
        return {"vendor": vendor, "topic": "vendor_guide", "source": file_path.name}
    elif name.startswith("rfc"):
        return {"vendor": "all", "topic": "rfc", "source": file_path.name}
    return {"vendor": "all", "topic": "general", "source": file_path.name}


def ingest():
    """Load protocol docs, chunk, embed, and store in ChromaDB."""
    md_files = sorted(DOCS_DIR.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {DOCS_DIR}")
        sys.exit(1)

    documents = []
    for fp in md_files:
        text = fp.read_text(encoding="utf-8")
        metadata = extract_metadata(fp)
        documents.append(Document(page_content=text, metadata=metadata))
    print(f"Loaded {len(documents)} document(s) from {DOCS_DIR}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    chunks = []
    for doc in documents:
        splits = splitter.split_documents([doc])
        for chunk in splits:
            chunk.metadata = doc.metadata.copy()
        chunks.extend(splits)
    print(f"Split into {len(chunks)} chunk(s)")

    embeddings = HuggingFaceEmbeddings(model_name=_EMBEDDING_MODEL)
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME,
    )
    print(f"Stored in ChromaDB at {CHROMA_DIR}")


if __name__ == "__main__":
    if "--clean" in sys.argv and CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
        print(f"Cleaned {CHROMA_DIR}")
    ingest()
