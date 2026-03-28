"""Scrapli SSH executor — multi-vendor, per-command connections."""
import asyncio
import logging
import os

from scrapli import AuthOptions, Cli, SessionOptions
from scrapli.exceptions import OpenException
from scrapli.transport import BinOptions
from scrapli.transport import Ssh2Options as TransportSsh2Options

from core.settings import (
    PASSWORD, SSH_RETRIES, SSH_RETRY_DELAY, SSH_STRICT_HOST_KEY, SSH_TIMEOUT_OPS, USERNAME,
)
from core.vault import get_secret

log = logging.getLogger("yanaa.transport.ssh")

_DEFINITIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "platforms", "definitions")
_CUSTOM_DEFINITIONS: dict[str, str] = {
    "mikrotik_routeros": os.path.join(_DEFINITIONS_DIR, "mikrotik_routeros.yaml"),
    "vyos_vyos":         os.path.join(_DEFINITIONS_DIR, "vyos_vyos.yaml"),
}


def _build_cli(device: dict, timeout_ops: int | None = None) -> Cli:
    platform = device["platform"]
    definition = _CUSTOM_DEFINITIONS.get(platform, platform)
    op_timeout = timeout_ops or SSH_TIMEOUT_OPS

    cli_style = device.get("cli_style", "")
    username = get_secret(f"yanaa/router{cli_style}", "username", quiet=True) or USERNAME
    password = get_secret(f"yanaa/router{cli_style}", "password", quiet=True) or PASSWORD

    if platform == "mikrotik_routeros":
        auth = AuthOptions(username=f"{username}+ct", password=password)
        session = SessionOptions(operation_timeout_s=op_timeout, return_char="\r\n")
    else:
        auth = AuthOptions(username=username, password=password)
        session = SessionOptions(operation_timeout_s=op_timeout)

    _known_hosts = os.path.expanduser("~/.ssh/known_hosts") if SSH_STRICT_HOST_KEY else None
    if platform == "vyos_vyos":
        transport = TransportSsh2Options(known_hosts_path=_known_hosts)
    elif SSH_STRICT_HOST_KEY:
        transport = BinOptions(enable_strict_key=True, known_hosts_path=_known_hosts)
    else:
        transport = BinOptions(enable_strict_key=False)

    return Cli(
        host=device["host"],
        definition_file_or_name=definition,
        auth_options=auth,
        session_options=session,
        transport_options=transport,
    )


async def execute_ssh(device: dict, command: str, timeout_ops: int | None = None) -> str:
    """Execute a show command via Scrapli SSH. Returns raw CLI output."""
    last_exc = None
    for attempt in range(1 + SSH_RETRIES):
        try:
            async with _build_cli(device, timeout_ops) as conn:
                log.debug("SSH → %s: %s", device["host"], command)
                result = await conn.send_input_async(input_=command)
            return result.result
        except OpenException:
            raise
        except Exception as e:
            last_exc = e
            if attempt < SSH_RETRIES:
                log.warning("SSH attempt %d/%d failed for %s: %s — retrying",
                            attempt + 1, 1 + SSH_RETRIES, device["host"], e)
                await asyncio.sleep(SSH_RETRY_DELAY)
    raise last_exc
