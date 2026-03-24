"""NetBox device inventory loader."""
import logging
import os

from core.vault import get_secret

log = logging.getLogger("netkb.netbox")


def load_devices() -> dict | None:
    """Load device inventory from NetBox.

    Returns {name: {host, platform, cli_style, vrf?}} or None if unavailable.
    """
    url = os.getenv("NETBOX_URL", "").strip()
    token = (get_secret("netkb/netbox", "token", fallback_env="NETBOX_TOKEN") or "").strip()

    if not url or not token:
        return None

    try:
        import pynetbox
        nb = pynetbox.api(url, token=token)
        nb.http_session.timeout = (5, 15)
        raw_devices = list(nb.dcim.devices.all())
    except Exception as exc:
        log.warning("NetBox unavailable: %s", exc)
        return None

    if not raw_devices:
        log.warning("NetBox returned no devices")
        return None

    devices: dict = {}
    for dev in raw_devices:
        try:
            name = dev.name
            if not name or not dev.primary_ip:
                continue

            host = dev.primary_ip.address.split("/")[0]
            platform = dev.platform.slug if dev.platform else ""
            cli_style = (dev.custom_fields or {}).get("cli_style", "")
            vrf = (dev.custom_fields or {}).get("vrf", "") or ""

            if not platform or not cli_style:
                log.warning("Device %s missing platform/cli_style — skipping", name)
                continue

            entry: dict = {"host": host, "platform": platform, "cli_style": cli_style}
            if vrf:
                entry["vrf"] = vrf
            devices[name] = entry
        except Exception as exc:
            log.warning("Device mapping error (skipping): %s", exc)

    if not devices:
        return None

    log.info("Loaded %d device(s) from NetBox", len(devices))
    return devices


def load_intent() -> dict | None:
    """Load network intent from NetBox config contexts.

    Expects config contexts named 'netkb-<device>' (per router) and
    optionally 'netkb-global' (containing autonomous_systems data).
    Falls back to 'dblcheck-<device>' prefix if netkb prefix not found.

    Returns {"autonomous_systems": {...}, "routers": {name: {...}, ...}}
    or None if unavailable.
    """
    url = os.getenv("NETBOX_URL", "").strip()
    token = (get_secret("netkb/netbox", "token", fallback_env="NETBOX_TOKEN") or "").strip()

    if not url or not token:
        return None

    try:
        import pynetbox
        nb = pynetbox.api(url, token=token)
        nb.http_session.timeout = (5, 15)
        # Try netkb prefix first, fall back to dblcheck prefix
        contexts = list(nb.extras.config_contexts.filter(name__isw="netkb-"))
        prefix = "netkb-"
        if not contexts:
            contexts = list(nb.extras.config_contexts.filter(name__isw="dblcheck-"))
            prefix = "dblcheck-"
    except Exception as exc:
        log.warning("NetBox config contexts unavailable: %s", exc)
        return None

    if not contexts:
        log.warning("NetBox: no config contexts found")
        return None

    autonomous_systems: dict = {}
    routers: dict = {}

    for ctx in contexts:
        name: str = ctx.name
        data: dict = ctx.data or {}

        if name == f"{prefix}global":
            autonomous_systems = data.get("autonomous_systems", data)
        elif name.startswith(prefix):
            device_name = name[len(prefix):]
            routers[device_name] = data

    if not routers:
        log.warning("NetBox: no per-device config contexts found")
        return None

    intent: dict = {"routers": routers}
    if autonomous_systems:
        intent["autonomous_systems"] = autonomous_systems

    log.info("Loaded intent for %d router(s) from NetBox config contexts", len(routers))
    return intent
