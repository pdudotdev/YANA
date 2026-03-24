"""Ingest OSPF knowledge base docs into ChromaDB via LangChain."""
import json
import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.netbox import load_devices, load_intent
from tools.rag import _CHROMA_DIR, _COLLECTION, _EMBEDDING_MODEL

DOCS_DIR = Path(__file__).parent / "docs"
LEGACY_DIR = Path(__file__).parent / "core" / "legacy"
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


def _router_to_markdown(name: str, router: dict) -> str:
    """Convert a single router's intent data to readable markdown."""
    lines = [f"## {name}"]
    lines.append(f"Roles: {', '.join(router.get('roles', []))}")
    lines.append(f"Platform: {router.get('platform', 'unknown')}, VRF: {router.get('vrf', 'global')}")

    ospf = router.get("igp", {}).get("ospf", {})
    if ospf:
        lines.append(f"OSPF Router ID: {ospf.get('router_id', 'N/A')}")
        area_type = ospf.get("area_type", "")
        area_types = ospf.get("area_types", {})
        areas = ospf.get("areas", {})
        area_parts = []
        for aid, nets in areas.items():
            atype = area_types.get(aid, area_type) or "normal"
            area_parts.append(f"Area {aid} {atype} ({', '.join(nets)})")
        if area_parts:
            lines.append(f"OSPF Areas: {'; '.join(area_parts)}")

    links = router.get("direct_links", {})
    if links:
        link_parts = [f"{peer} ({info['local_interface']}, {info['local_ip']})"
                      for peer, info in links.items()]
        lines.append(f"Direct Links: {', '.join(link_parts)}")

    bgp = router.get("bgp", {})
    if bgp:
        asn = router.get("asn", "")
        neighbors = bgp.get("neighbors", {})
        if asn:
            lines.append(f"BGP AS: {asn}")
        if neighbors:
            bgp_parts = [f"{peer} (AS {info['as']}, {info['peer']})"
                         for peer, info in neighbors.items()]
            lines.append(f"BGP Neighbors: {', '.join(bgp_parts)}")

    return "\n".join(lines)


def load_network_context() -> list[Document]:
    """Load intent and inventory from NetBox, falling back to legacy JSON files."""
    documents = []

    # ── Intent (NetBox config contexts → fallback to INTENT.json) ────────
    intent = load_intent()
    if intent:
        source = "NetBox"
        for name, router in intent.get("routers", {}).items():
            documents.append(Document(
                page_content=_router_to_markdown(name, router),
                metadata={"vendor": "all", "topic": "intent", "source": "NetBox config context"},
            ))
    else:
        intent_path = LEGACY_DIR / "INTENT.json"
        if intent_path.exists():
            source = intent_path.name
            intent = json.loads(intent_path.read_text())
            for name, router in intent.get("routers", {}).items():
                documents.append(Document(
                    page_content=_router_to_markdown(name, router),
                    metadata={"vendor": "all", "topic": "intent", "source": "INTENT.json"},
                ))
    intent_count = len(documents)
    if intent_count:
        print(f"Loaded {intent_count} router intent(s) from {source}")

    # ── Inventory (NetBox devices → fallback to NETWORK.json) ────────────
    inventory = load_devices()
    if inventory:
        source = "NetBox"
    else:
        network_path = LEGACY_DIR / "NETWORK.json"
        if network_path.exists():
            source = network_path.name
            inventory = json.loads(network_path.read_text())

    if inventory:
        lines = ["## Network Inventory\n"]
        for name, info in sorted(inventory.items()):
            vrf = info.get("vrf", "global")
            host = info.get("host", "N/A")
            platform = info.get("platform", "N/A")
            cli_style = info.get("cli_style", "N/A")
            lines.append(f"- {name}: {host}, {platform}, {cli_style}, VRF={vrf}")
        documents.append(Document(
            page_content="\n".join(lines),
            metadata={"vendor": "all", "topic": "inventory", "source": source},
        ))
        print(f"Loaded inventory ({len(inventory)} devices) from {source}")

    return documents


def ingest():
    """Load docs, chunk, embed, and store in ChromaDB."""
    md_files = sorted(DOCS_DIR.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {DOCS_DIR}")
        sys.exit(1)

    # Load documents with metadata
    documents = []
    for fp in md_files:
        text = fp.read_text(encoding="utf-8")
        metadata = extract_metadata(fp)
        documents.append(Document(page_content=text, metadata=metadata))
    print(f"Loaded {len(documents)} document(s) from {DOCS_DIR}")

    # Load network context (NetBox → fallback to legacy JSON)
    documents.extend(load_network_context())

    # Split into chunks
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

    # Embed and store
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
