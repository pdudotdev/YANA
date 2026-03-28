"""Device inventory — NetBox primary, core/legacy/NETWORK.json fallback."""
import json
import logging
from pathlib import Path

from core.netbox import load_devices

_log = logging.getLogger("netkb.inventory")
_NETWORK_JSON = Path(__file__).parent / "legacy" / "NETWORK.json"

_netbox_result = load_devices()
if _netbox_result:
    devices: dict = _netbox_result
    source: str = "netbox"
    _log.info("Inventory: loaded %d device(s) from NetBox", len(devices))
elif _NETWORK_JSON.exists():
    try:
        devices = json.loads(_NETWORK_JSON.read_text())
        source = "network_json"
        _log.info("Inventory: loaded %d device(s) from %s", len(devices), _NETWORK_JSON.name)
    except (json.JSONDecodeError, OSError) as exc:
        _log.error("Failed to parse %s: %s", _NETWORK_JSON.name, exc)
        devices = {}
        source = "empty"
else:
    devices = {}
    source = "empty"
    _log.error("No inventory — check NETBOX_URL and NETBOX_TOKEN")


def get_device(name: str) -> dict:
    """Return device dict for name, raising KeyError with known device list on miss."""
    if name not in devices:
        known = ", ".join(sorted(devices)) or "(none loaded)"
        raise KeyError(f"Unknown device {name!r} — known: {known}")
    return devices[name]
