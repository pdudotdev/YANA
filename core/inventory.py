"""Device inventory — loaded from data/NETWORK.json."""
import json
import logging
from pathlib import Path

_log = logging.getLogger("yana.inventory")
_NETWORK_JSON = Path(__file__).parent.parent / "data" / "NETWORK.json"

if _NETWORK_JSON.exists():
    try:
        devices: dict = json.loads(_NETWORK_JSON.read_text())
        source: str = "network_json"
        _log.info("Inventory: loaded %d device(s) from %s", len(devices), _NETWORK_JSON.name)
    except (json.JSONDecodeError, OSError) as exc:
        _log.error("Failed to parse %s: %s", _NETWORK_JSON.name, exc)
        devices = {}
        source = "empty"
else:
    devices = {}
    source = "empty"
    _log.error("No inventory — add data/NETWORK.json")


def get_device(name: str) -> dict:
    """Return device dict for name, raising KeyError with known device list on miss."""
    if name not in devices:
        known = ", ".join(sorted(devices)) or "(none loaded)"
        raise KeyError(f"Unknown device {name!r} — known: {known}")
    return devices[name]
