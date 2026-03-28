"""UT-004: Transport dispatcher."""
from unittest.mock import AsyncMock, patch


class TestExecuteCommand:
    async def test_success_returns_structured_dict(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.return_value = "Neighbor ID  State  Interface\n1.1.1.1  FULL  Eth0/1"
            from transport import execute_command
            result = await execute_command("R1", "show ip ospf neighbor")
        assert result["device"] == "R1"
        assert result["cli_style"] == "ios"
        assert result["_command"] == "show ip ospf neighbor"
        assert "FULL" in result["raw"]

    async def test_unknown_device_error_shape(self):
        """Unknown device error has only 'error' key with descriptive message."""
        from transport import execute_command
        result = await execute_command("NONEXISTENT", "show version")
        assert set(result.keys()) == {"error"}
        assert "Unknown device" in result["error"]

    async def test_ssh_failure_error_shape(self):
        """SSH failure error includes device and cli_style alongside error."""
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.side_effect = TimeoutError("SSH timeout")
            from transport import execute_command
            result = await execute_command("R1", "show version")
        assert "error" in result
        assert "device" in result
        assert "cli_style" in result

    async def test_ssh_error_returns_error_dict(self):
        with patch("transport.execute_ssh", new_callable=AsyncMock) as mock_ssh:
            mock_ssh.side_effect = ConnectionError("SSH timeout")
            from transport import execute_command
            result = await execute_command("R1", "show ip ospf neighbor")
        assert result["device"] == "R1"
        assert result["cli_style"] == "ios"
        assert "error" in result
        assert "SSH timeout" in result["error"]
