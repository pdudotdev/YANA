"""Transport dispatcher — routes execute_command calls to SSH."""
import asyncio
import logging

from core.inventory import devices
from core.settings import SSH_MAX_CONCURRENT
from transport.ssh import execute_ssh

log = logging.getLogger("netkb.transport")

_cmd_sem = asyncio.Semaphore(SSH_MAX_CONCURRENT)


async def execute_command(device_name: str, command: str,
                          timeout_ops: int | None = None) -> dict:
    """Execute a read command on a device and return a structured result dict."""
    device = devices.get(device_name)
    if not device:
        return {"error": f"Unknown device: {device_name}"}

    async with _cmd_sem:
        try:
            raw_output = await execute_ssh(device, command, timeout_ops=timeout_ops)
        except Exception as e:
            log.error("command failed: %s — %s", device_name, e)
            return {"device": device_name, "cli_style": device["cli_style"], "error": str(e)}

    return {
        "device": device_name,
        "_command": command,
        "cli_style": device["cli_style"],
        "raw": raw_output,
    }
