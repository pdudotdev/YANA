"""Routing table and policy diagnostic tool."""
from core.inventory import get_device
from input_models.models import RoutingQuery
from platforms.platform_map import get_action
from tools import _error_response
from transport import execute_command


async def get_routing(params: RoutingQuery) -> dict:
    """Retrieve routing table and policy data from a network device.

    Supported queries:
    - ip_route             — IP routing table (VRF-aware on supported platforms)
    - route_maps           — Route map / routing policy definitions
    - prefix_lists         — Prefix list definitions
    - policy_based_routing — Policy-based routing rules
    - access_lists         — Access control lists
    """
    try:
        device = get_device(params.device)
    except KeyError as exc:
        return _error_response(params.device, str(exc))

    try:
        action = get_action(device, "routing_table", params.query, vrf=params.vrf)
    except KeyError:
        return _error_response(params.device, f"Routing query '{params.query}' not supported on {device['cli_style'].upper()}")

    return await execute_command(params.device, action)
