"""Network intent query tool."""
import asyncio
import json
import logging

from input_models.models import IntentQuery
from tools import INTENT_JSON as _INTENT_JSON, _error_response

log = logging.getLogger("yana.intent")


def _load_intent() -> dict | None:
    """Load intent from the JSON file."""
    if _INTENT_JSON.exists():
        try:
            return json.loads(_INTENT_JSON.read_text())
        except Exception as exc:
            log.warning("Failed to load INTENT.json: %s", exc)
    return None


async def query_intent(params: IntentQuery) -> dict:
    """Retrieve network design intent for a device or the full topology.

    Returns structured intent data including OSPF areas, BGP neighbors,
    routing policies, and role assignments from the intent JSON file.

    If no device is specified, returns intent for all devices.
    """
    intent = await asyncio.to_thread(_load_intent)
    if not intent:
        return _error_response(None, "Intent unavailable — add data/INTENT.json")

    if params.device is None:
        return intent

    routers = intent.get("routers", {})
    if params.device not in routers:
        known = ", ".join(sorted(routers)) or "(none)"
        return _error_response(params.device, f"Unknown device {params.device!r} — known: {known}")

    return {"device": params.device, "intent": routers[params.device]}
