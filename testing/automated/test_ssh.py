"""UT-008: SSH layer — _build_cli construction and execute_ssh retry logic."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from transport.ssh import _build_cli, execute_ssh


IOS_DEVICE = {"host": "10.0.0.1", "platform": "cisco_iosxe", "cli_style": "ios"}
MIKROTIK_DEVICE = {"host": "10.0.0.5", "platform": "mikrotik_routeros", "cli_style": "routeros"}
VYOS_DEVICE = {"host": "10.0.0.6", "platform": "vyos_vyos", "cli_style": "vyos"}


def _async_cm(raw_result: str):
    """Build a fake Scrapli Cli async context manager returning raw_result."""
    mock_conn = AsyncMock()
    mock_conn.send_input_async.return_value = MagicMock(result=raw_result)
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=mock_conn)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


def _failing_cm(exc):
    """Build a fake Cli whose __aenter__ raises exc."""
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(side_effect=exc)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


# ── _build_cli() ──────────────────────────────────────────────────────────────

class TestBuildCli:
    def test_mikrotik_username_gets_ct_suffix(self):
        with patch("transport.ssh.USERNAME", "admin"), \
             patch("transport.ssh.PASSWORD", "pass"), \
             patch("transport.ssh.Cli") as mock_cli, \
             patch("transport.ssh.BinOptions"):
            _build_cli(MIKROTIK_DEVICE)
        auth = mock_cli.call_args.kwargs["auth_options"]
        assert auth.username == "admin+ct"

    def test_mikrotik_session_return_char(self):
        with patch("transport.ssh.Cli") as mock_cli, \
             patch("transport.ssh.BinOptions"):
            _build_cli(MIKROTIK_DEVICE)
        session = mock_cli.call_args.kwargs["session_options"]
        assert session.return_char == "\r\n"

    def test_standard_device_uses_binoptions(self):
        with patch("transport.ssh.BinOptions") as mock_bin, \
             patch("transport.ssh.Cli"):
            _build_cli(IOS_DEVICE)
        mock_bin.assert_called_once()

    def test_vyos_uses_ssh2options(self):
        with patch("transport.ssh.TransportSsh2Options") as mock_ssh2, \
             patch("transport.ssh.Cli"):
            _build_cli(VYOS_DEVICE)
        mock_ssh2.assert_called_once()

    def test_global_credentials_used(self):
        with patch("transport.ssh.USERNAME", "global_user"), \
             patch("transport.ssh.PASSWORD", "global_pass"), \
             patch("transport.ssh.BinOptions"), \
             patch("transport.ssh.Cli") as mock_cli:
            _build_cli(IOS_DEVICE)
        auth = mock_cli.call_args.kwargs["auth_options"]
        assert auth.username == "global_user"
        assert auth.password == "global_pass"


# ── execute_ssh() ─────────────────────────────────────────────────────────────

class TestExecuteSsh:
    async def test_success_returns_raw_string(self):
        with patch("transport.ssh._build_cli", return_value=_async_cm("Neighbor  FULL")):
            result = await execute_ssh(IOS_DEVICE, "show ip ospf neighbor")
        assert result == "Neighbor  FULL"

    async def test_open_exception_immediately_reraised_without_retry(self):
        """OpenException must NOT trigger the retry loop — it propagates immediately."""
        from scrapli.exceptions import OpenException

        build_call_count = 0

        def counting_build(*args, **kwargs):
            nonlocal build_call_count
            build_call_count += 1
            return _failing_cm(OpenException("connection refused"))

        with patch("transport.ssh._build_cli", side_effect=counting_build), \
             patch("transport.ssh.SSH_RETRIES", 1):
            with pytest.raises(OpenException):
                await execute_ssh(IOS_DEVICE, "show version")

        assert build_call_count == 1  # no retry

    async def test_generic_exception_retries_and_recovers(self):
        """A transient failure on attempt 1 is retried; success on attempt 2 is returned."""
        attempt = 0

        def flaky_build(*args, **kwargs):
            nonlocal attempt
            attempt += 1
            if attempt == 1:
                return _failing_cm(ConnectionError("transient"))
            return _async_cm("recovered output")

        with patch("transport.ssh._build_cli", side_effect=flaky_build), \
             patch("transport.ssh.SSH_RETRIES", 1), \
             patch("transport.ssh.SSH_RETRY_DELAY", 0):
            result = await execute_ssh(IOS_DEVICE, "show version")

        assert result == "recovered output"
        assert attempt == 2

    async def test_all_retries_exhausted_raises_last_exception(self):
        with patch("transport.ssh._build_cli", return_value=_failing_cm(TimeoutError("SSH timeout"))), \
             patch("transport.ssh.SSH_RETRIES", 1), \
             patch("transport.ssh.SSH_RETRY_DELAY", 0):
            with pytest.raises(TimeoutError, match="SSH timeout"):
                await execute_ssh(IOS_DEVICE, "show version")
