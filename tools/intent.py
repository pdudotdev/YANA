"""Network intent query tool."""
import json
import logging
from pathlib import Path

from core.netbox import load_intent
from input_models.models import IntentQuery
from tools import _error_response

log = logging.getLogger("netkb.intent")

_INTENT_JSON = Path(__file__).resolve().parent.parent / "core" / "legacy" / "INTENT.json"


def _load_intent() -> dict | None:
    """Load intent from NetBox, falling back to the legacy JSON file."""
    result = load_intent()
    if result:
        return result
    if _INTENT_JSON.exists():
        try:
            return json.loads(_INTENT_JSON.read_text())
        except Exception as exc:
            log.warning("Failed to load legacy INTENT.json: %s", exc)
    return None


async def query_intent(params: IntentQuery) -> dict:
    """Retrieve network design intent for a device or the full topology.

    Returns structured intent data including OSPF areas, BGP neighbors,
    routing policies, and role assignments from NetBox config contexts.

    If no device is specified, returns intent for all devices.
    """
    intent = _load_intent()
    if not intent:
        return _error_response(None, "Intent unavailable — check NETBOX_URL/NETBOX_TOKEN or INTENT.json")

    if params.device is None:
        return intent

    routers = intent.get("routers", {})
    if params.device not in routers:
        known = ", ".join(sorted(routers)) or "(none)"
        return _error_response(params.device, f"Unknown device {params.device!r} — known: {known}")

    return {"device": params.device, "intent": routers[params.device]}
