"""UT-010: core/inventory.py — get_device() and source tracking."""
import pytest

import core.inventory as _inv
_real_get_device = _inv.get_device


class TestGetDevice:
    def test_known_device_returns_dict(self, monkeypatch):
        import core.inventory
        monkeypatch.setattr(core.inventory, "get_device", _real_get_device)
        result = core.inventory.get_device("R1")
        assert result["cli_style"] == "ios"
        assert result["host"] == "10.0.0.1"

    def test_error_lists_known_devices(self, monkeypatch):
        import core.inventory
        monkeypatch.setattr(core.inventory, "get_device", _real_get_device)
        with pytest.raises(KeyError) as exc_info:
            core.inventory.get_device("GHOST")
        msg = str(exc_info.value)
        assert "R1" in msg or "known" in msg

    def test_empty_inventory_error_message(self, monkeypatch):
        import core.inventory
        monkeypatch.setattr(core.inventory, "devices", {})
        monkeypatch.setattr(core.inventory, "get_device", _real_get_device)
        with pytest.raises(KeyError) as exc_info:
            core.inventory.get_device("R1")
        assert "none loaded" in str(exc_info.value)
