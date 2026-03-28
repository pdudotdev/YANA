"""Operational tools: get_interfaces, traceroute."""
from core.inventory import get_device
from core.settings import SSH_TIMEOUT_OPS_LONG
from input_models.models import InterfacesQuery, TracerouteInput
from platforms.platform_map import get_action
from tools import _error_response
from transport import execute_command


async def get_interfaces(params: InterfacesQuery) -> dict:
    """Retrieve interface status and IP information from a device.

    Use to verify interface state, IP assignments, and link status.
    """
    try:
        device = get_device(params.device)
    except KeyError as exc:
        return _error_response(params.device, str(exc))

    try:
        action = get_action(device, "interfaces", "interface_status")
    except KeyError:
        return _error_response(params.device, f"Interface status not supported on {device['cli_style'].upper()}")

    return await execute_command(params.device, action)


async def traceroute(params: TracerouteInput) -> dict:
    """Trace the forwarding path from a device to a destination IP.

    Pass source to force the traceroute to use a specific source address,
    ensuring the probe follows the monitored path rather than an alternate route.
    """
    try:
        device = get_device(params.device)
    except KeyError as exc:
        return _error_response(params.device, str(exc))

    try:
        base_cmd = get_action(device, "tools", "traceroute", vrf=params.vrf)
    except KeyError:
        return _error_response(params.device, f"Traceroute not supported on {device['cli_style'].upper()}")

    cli_style = device["cli_style"]

    if cli_style == "routeros":
        command = f"{base_cmd} address={params.destination}"
        if params.source:
            command += f" src-address={params.source}"
    elif cli_style == "aos":
        # AOS-CX syntax: traceroute <dest> [vrf <name>] [source <src>] [probes <n>] [timeout <s>]
        command = f"traceroute {params.destination}"
        vrf_name = params.vrf or device.get("vrf")
        if vrf_name and vrf_name.lower() != "default":
            command += f" vrf {vrf_name}"
        if params.source:
            command += f" source {params.source}"
        command += " probes 1 timeout 2"
    else:
        command = f"{base_cmd} {params.destination}"
        if params.source:
            command += f" source {params.source}"
        if cli_style == "ios":
            command += " probe 1 timeout 2"

    return await execute_command(params.device, command, timeout_ops=SSH_TIMEOUT_OPS_LONG)
