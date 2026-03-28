"""Backend status tool."""
import asyncio
import logging

import core.inventory
import core.vault
from core.netbox import load_intent
from tools import CHROMA_DIR as _CHROMA_DIR, INTENT_JSON as _INTENT_JSON

log = logging.getLogger("yanaa.status")


async def get_status() -> dict:
    """Report which backend each subsystem is using.

    Probes inventory, credentials, intent, and the ChromaDB vector store
    and returns their current source/availability.
    """
    # Inventory
    device_count = len(core.inventory.devices)
    inventory_status = {
        "source": core.inventory.source,
        "device_count": device_count,
    }

    # Vault / credentials
    # Trigger secret resolution so _sources is populated (no-op if already cached)
    core.vault.get_secret("yanaa/router", "username", fallback_env="ROUTER_USERNAME", quiet=True)
    vault_status = {"source": core.vault.get_source("yanaa/router")}

    # Intent
    intent = await asyncio.to_thread(load_intent)
    if intent:
        intent_status = {
            "source": "netbox",
            "router_count": len(intent.get("routers", {})),
        }
    elif _INTENT_JSON.exists():
        intent_status = {"source": "intent_json"}
    else:
        intent_status = {"source": "unavailable"}

    # ChromaDB
    chroma_available = _CHROMA_DIR.exists() and any(_CHROMA_DIR.iterdir())
    chroma_status = {"available": chroma_available}

    return {
        "inventory": inventory_status,
        "vault": vault_status,
        "intent": intent_status,
        "chromadb": chroma_status,
    }
