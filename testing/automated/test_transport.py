"""UT-004: Transport dispatcher."""
import asyncio
from unittest.mock import AsyncMock, patch

import pytest


class TestExecuteCommand:
    def test_unknown_device(self):
        from transport import execute_command
        result = asyncio.get_event_loop().run_until_complete(
            execute_command("NONEXISTENT", "show ip ospf neighbor")
        )
        assert "error" in result
        assert "Unknown device" in result["error"]

    def test_success_returns_structured_dict(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "Neighbor ID  State  Interface\n1.1.1.1  FULL  Eth0/1"
            from transport import execute_command
            result = asyncio.get_event_loop().run_until_complete(
                execute_command("R1", "show ip ospf neighbor")
            )
        assert result["device"] == "R1"
        assert result["cli_style"] == "ios"
        assert result["_command"] == "show ip ospf neighbor"
        assert "FULL" in result["raw"]

    def test_ssh_error_returns_error_dict(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.side_effect = ConnectionError("SSH timeout")
            from transport import execute_command
            result = asyncio.get_event_loop().run_until_complete(
                execute_command("R1", "show ip ospf neighbor")
            )
        assert result["device"] == "R1"
        assert result["cli_style"] == "ios"
        assert "error" in result
        assert "SSH timeout" in result["error"]
