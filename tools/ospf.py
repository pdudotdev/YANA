"""OSPF diagnostic tool."""
from core.inventory import devices
from input_models.models import OspfQuery
from platforms.platform_map import get_action
from tools import _error_response
from transport import execute_command


async def get_ospf(params: OspfQuery) -> dict:
    """Retrieve OSPF operational data from a network device.

    Supported queries:
    - neighbors   — OSPF neighbor state and adjacency health
    - database    — LSDB contents and LSA propagation
    - borders     — ABR/ASBR identification
    - config      — OSPF configuration on the device
    - interfaces  — OSPF-enabled interfaces and parameters (timers, area, cost)
    - details     — Process-level details (router-id, SPF stats)
    """
    device = devices.get(params.device)
    if not device:
        return _error_response(params.device, f"Unknown device: {params.device}")

    try:
        action = get_action(device, "ospf", params.query, vrf=params.vrf)
    except KeyError:
        return _error_response(params.device, f"OSPF query '{params.query}' not supported on {device['cli_style'].upper()}")

    return await execute_command(params.device, action)
