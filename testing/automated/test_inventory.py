"""UT-010: core/inventory.py — get_device() and source tracking."""
import pytest

# Capture the real function at module import time, before conftest's autouse
# fixture patches core.inventory.get_device with a mock.
import core.inventory as _inv
_real_get_device = _inv.get_device


class TestGetDevice:
    def test_known_device_returns_dict(self):
        from core.inventory import get_device
        result = get_device("R1")
        assert result["cli_style"] == "ios"
        assert result["host"] == "10.0.0.1"

    def test_unknown_device_raises_key_error(self):
        from core.inventory import get_device
        with pytest.raises(KeyError) as exc_info:
            get_device("NONEXISTENT")
        assert "NONEXISTENT" in str(exc_info.value)

    def test_error_lists_known_devices(self):
        from core.inventory import get_device
        with pytest.raises(KeyError) as exc_info:
            get_device("GHOST")
        msg = str(exc_info.value)
        # Known devices from MOCK_DEVICES (R1–R6) should appear
        assert "R1" in msg or "known" in msg

    def test_empty_inventory_error_message(self, monkeypatch):
        import core.inventory
        monkeypatch.setattr(core.inventory, "devices", {})
        monkeypatch.setattr(core.inventory, "get_device", _real_get_device)
        with pytest.raises(KeyError) as exc_info:
            core.inventory.get_device("R1")
        assert "none loaded" in str(exc_info.value)


class TestInventorySource:
    def test_source_attribute_exists(self):
        import core.inventory
        assert hasattr(core.inventory, "source")
        assert core.inventory.source in ("netbox", "network_json", "empty")

    def test_source_is_netbox_when_mocked(self):
        # conftest patches source to "netbox"
        import core.inventory
        assert core.inventory.source == "netbox"
