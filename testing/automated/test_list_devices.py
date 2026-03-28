"""UT-011: list_devices tool."""
import pytest

from input_models.models import DeviceListQuery
from tools.inventory_tool import list_devices


class TestListDevices:
    async def test_returns_all_devices(self):
        result = await list_devices(DeviceListQuery())
        assert "devices" in result
        assert set(result["devices"].keys()) == {"R1", "R2", "R3", "R4", "R5", "R6"}

    async def test_filter_by_cli_style(self):
        result = await list_devices(DeviceListQuery(cli_style="eos"))
        assert "devices" in result
        assert list(result["devices"].keys()) == ["R2"]
        assert result["devices"]["R2"]["cli_style"] == "eos"

    async def test_filter_ios(self):
        result = await list_devices(DeviceListQuery(cli_style="ios"))
        assert "devices" in result
        assert list(result["devices"].keys()) == ["R1"]

    async def test_filter_no_match(self):
        result = await list_devices(DeviceListQuery(cli_style="unknown_style"))
        assert "error" in result

    async def test_empty_inventory(self, monkeypatch):
        import tools.inventory_tool
        monkeypatch.setattr(tools.inventory_tool, "devices", {})
        result = await list_devices(DeviceListQuery())
        assert "error" in result

    async def test_device_fields_present(self):
        result = await list_devices(DeviceListQuery())
        for device in result["devices"].values():
            assert "host" in device
            assert "cli_style" in device
