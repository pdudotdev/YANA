"""Device inventory — loads from NetBox at import time."""
import logging

from core.netbox import load_devices

_log = logging.getLogger("netkb.inventory")

_netbox_result = load_devices()
if _netbox_result:
    devices: dict = _netbox_result
    _log.info("Inventory: loaded %d device(s) from NetBox", len(devices))
else:
    _log.error("No inventory — check NETBOX_URL and NETBOX_TOKEN")
    devices: dict = {}
