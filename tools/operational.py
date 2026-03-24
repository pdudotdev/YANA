"""Operational tool: get_interfaces."""
from core.inventory import devices
from input_models.models import InterfacesQuery
from platforms.platform_map import get_action
from tools import _error_response
from transport import execute_command


async def get_interfaces(params: InterfacesQuery) -> dict:
    """Retrieve interface status and IP information from a device.

    Use to verify interface state, IP assignments, and link status.
    """
    device = devices.get(params.device)
    if not device:
        return _error_response(params.device, f"Unknown device: {params.device}")

    try:
        action = get_action(device, "interfaces", "interface_status")
    except KeyError:
        return _error_response(params.device, f"Interface status not supported on {device['cli_style'].upper()}")

    return await execute_command(params.device, action)
