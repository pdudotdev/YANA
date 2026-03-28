"""Device inventory listing tool."""
from core.inventory import devices
from input_models.models import DeviceListQuery
from tools import _error_response


async def list_devices(params: DeviceListQuery) -> dict:
    """Return the device inventory, optionally filtered by CLI style.

    Pass cli_style to narrow results to a specific vendor family
    (e.g. 'eos' for Arista, 'ios' for Cisco). Omit to return all devices.
    """
    if not devices:
        return _error_response(None, "Device inventory is empty")

    if params.cli_style:
        result = {k: v for k, v in devices.items() if v.get("cli_style") == params.cli_style}
        if not result:
            return _error_response(None, f"No devices found with cli_style={params.cli_style!r}")
        return {"devices": result}

    return {"devices": devices}
