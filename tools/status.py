"""Backend status tool."""
import json
import logging

import core.inventory
from tools import CHROMA_DIR as _CHROMA_DIR, INTENT_JSON as _INTENT_JSON

log = logging.getLogger("yana.status")


async def get_status() -> dict:
    """Report which backend each subsystem is using.

    Probes inventory, intent, and the ChromaDB vector store
    and returns their current source/availability.
    """
    # Inventory
    device_count = len(core.inventory.devices)
    inventory_status = {
        "source": core.inventory.source,
        "device_count": device_count,
    }

    # Intent
    if _INTENT_JSON.exists():
        try:
            data = json.loads(_INTENT_JSON.read_text())
            intent_status = {
                "source": "intent_json",
                "router_count": len(data.get("routers", {})),
            }
        except Exception:
            intent_status = {"source": "unavailable"}
    else:
        intent_status = {"source": "unavailable"}

    # ChromaDB
    chroma_available = _CHROMA_DIR.exists() and any(_CHROMA_DIR.iterdir())
    chroma_status = {"available": chroma_available}

    return {
        "inventory": inventory_status,
        "intent": intent_status,
        "chromadb": chroma_status,
    }
