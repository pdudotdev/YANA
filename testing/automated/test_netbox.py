"""UT-007: NetBox inventory and intent loader."""
from unittest.mock import MagicMock, patch

from core.netbox import load_devices, load_intent


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_nb_device(name="R1", ip="10.0.0.1/32", platform_slug="cisco_iosxe",
                    cli_style="ios", vrf=""):
    """Build a mock pynetbox device record."""
    dev = MagicMock()
    dev.name = name
    dev.primary_ip = MagicMock()
    dev.primary_ip.address = ip
    dev.platform = MagicMock()
    dev.platform.slug = platform_slug
    dev.custom_fields = {"cli_style": cli_style, "vrf": vrf}
    return dev


def _make_pynetbox(devices=None, contexts=None):
    """Return (mock_module, mock_nb_client) pre-configured with devices/contexts."""
    mock_nb = MagicMock()
    mock_nb.dcim.devices.all.return_value = devices if devices is not None else []
    mock_nb.extras.config_contexts.filter.return_value = contexts if contexts is not None else []

    mock_module = MagicMock()
    mock_module.api.return_value = mock_nb
    return mock_module, mock_nb


# ── load_devices() ────────────────────────────────────────────────────────────

class TestLoadDevices:
    def test_no_netbox_url_returns_none(self, monkeypatch):
        monkeypatch.delenv("NETBOX_URL", raising=False)
        with patch("core.netbox.get_secret", return_value="token"):
            result = load_devices()
        assert result is None

    def test_no_netbox_token_returns_none(self, monkeypatch):
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        with patch("core.netbox.get_secret", return_value=None):
            monkeypatch.delenv("NETBOX_TOKEN", raising=False)
            result = load_devices()
        assert result is None

    def test_pynetbox_exception_returns_none(self, monkeypatch):
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        mock_module = MagicMock()
        mock_module.api.side_effect = ConnectionError("refused")
        with patch("core.netbox.get_secret", return_value="token"), \
             patch.dict("sys.modules", {"pynetbox": mock_module}):
            result = load_devices()
        assert result is None

    def test_empty_device_list_returns_none(self, monkeypatch):
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        mock_module, _ = _make_pynetbox(devices=[])
        with patch("core.netbox.get_secret", return_value="token"), \
             patch.dict("sys.modules", {"pynetbox": mock_module}):
            result = load_devices()
        assert result is None

    def test_valid_device_parsed_correctly(self, monkeypatch):
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        dev = _make_nb_device("R1", "10.0.0.1/32", "cisco_iosxe", "ios")
        mock_module, _ = _make_pynetbox(devices=[dev])
        with patch("core.netbox.get_secret", return_value="token"), \
             patch.dict("sys.modules", {"pynetbox": mock_module}):
            result = load_devices()
        assert result is not None
        assert "R1" in result
        assert result["R1"]["host"] == "10.0.0.1"
        assert result["R1"]["platform"] == "cisco_iosxe"
        assert result["R1"]["cli_style"] == "ios"
        assert "vrf" not in result["R1"]  # empty vrf → not included

    def test_device_with_vrf_included(self, monkeypatch):
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        dev = _make_nb_device("R2", vrf="MGMT")
        mock_module, _ = _make_pynetbox(devices=[dev])
        with patch("core.netbox.get_secret", return_value="token"), \
             patch.dict("sys.modules", {"pynetbox": mock_module}):
            result = load_devices()
        assert result["R2"]["vrf"] == "MGMT"

    def test_device_missing_primary_ip_skipped(self, monkeypatch):
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        bad = MagicMock()
        bad.name = "NoPrimary"
        bad.primary_ip = None
        good = _make_nb_device("Good")
        mock_module, _ = _make_pynetbox(devices=[bad, good])
        with patch("core.netbox.get_secret", return_value="token"), \
             patch.dict("sys.modules", {"pynetbox": mock_module}):
            result = load_devices()
        assert "NoPrimary" not in result
        assert "Good" in result

    def test_device_missing_cli_style_skipped(self, monkeypatch):
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        bad = _make_nb_device("NoCli", cli_style="")
        good = _make_nb_device("Good")
        mock_module, _ = _make_pynetbox(devices=[bad, good])
        with patch("core.netbox.get_secret", return_value="token"), \
             patch.dict("sys.modules", {"pynetbox": mock_module}):
            result = load_devices()
        assert "NoCli" not in result
        assert "Good" in result

    def test_per_device_exception_does_not_abort(self, monkeypatch):
        """A broken device entry is skipped; valid devices still load."""
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        bad = MagicMock()
        bad.name = "Broken"
        bad.primary_ip.address.split.side_effect = AttributeError("boom")
        good = _make_nb_device("Good")
        mock_module, _ = _make_pynetbox(devices=[bad, good])
        with patch("core.netbox.get_secret", return_value="token"), \
             patch.dict("sys.modules", {"pynetbox": mock_module}):
            result = load_devices()
        assert "Good" in result


# ── load_intent() ─────────────────────────────────────────────────────────────

class TestLoadIntent:
    def test_no_netbox_url_returns_none(self, monkeypatch):
        monkeypatch.delenv("NETBOX_URL", raising=False)
        with patch("core.netbox.get_secret", return_value="token"):
            result = load_intent()
        assert result is None

    def test_no_contexts_returns_none(self, monkeypatch):
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        mock_module, mock_nb = _make_pynetbox(contexts=[])
        # Both yanaa- and dblcheck- return empty
        mock_nb.extras.config_contexts.filter.return_value = []
        with patch("core.netbox.get_secret", return_value="token"), \
             patch.dict("sys.modules", {"pynetbox": mock_module}):
            result = load_intent()
        assert result is None

    def test_yanaa_prefix_parsed(self, monkeypatch):
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        ctx = MagicMock()
        ctx.name = "yanaa-R1"
        ctx.data = {"roles": ["ABR"], "platform": "cisco_iosxe"}
        mock_module, _ = _make_pynetbox(contexts=[ctx])
        with patch("core.netbox.get_secret", return_value="token"), \
             patch.dict("sys.modules", {"pynetbox": mock_module}):
            result = load_intent()
        assert result is not None
        assert "R1" in result["routers"]
        assert result["routers"]["R1"]["roles"] == ["ABR"]

    def test_fallback_to_dblcheck_prefix(self, monkeypatch):
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        ctx = MagicMock()
        ctx.name = "dblcheck-R1"
        ctx.data = {"roles": ["LEAF"]}

        def filter_side_effect(name__isw=None):
            if name__isw == "yanaa-":
                return []
            return [ctx]

        mock_module, mock_nb = _make_pynetbox()
        mock_nb.extras.config_contexts.filter.side_effect = filter_side_effect
        with patch("core.netbox.get_secret", return_value="token"), \
             patch.dict("sys.modules", {"pynetbox": mock_module}):
            result = load_intent()
        assert result is not None
        assert "R1" in result["routers"]

    def test_global_context_provides_autonomous_systems(self, monkeypatch):
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        ctx_global = MagicMock()
        ctx_global.name = "yanaa-global"
        ctx_global.data = {"autonomous_systems": {"1010": {"name": "AS1010"}}}
        ctx_dev = MagicMock()
        ctx_dev.name = "yanaa-R1"
        ctx_dev.data = {"roles": ["CORE"]}
        mock_module, _ = _make_pynetbox(contexts=[ctx_global, ctx_dev])
        with patch("core.netbox.get_secret", return_value="token"), \
             patch.dict("sys.modules", {"pynetbox": mock_module}):
            result = load_intent()
        assert "autonomous_systems" in result
        assert "1010" in result["autonomous_systems"]
        assert "R1" in result["routers"]

    def test_pynetbox_exception_returns_none(self, monkeypatch):
        monkeypatch.setenv("NETBOX_URL", "http://netbox")
        mock_module = MagicMock()
        mock_module.api.side_effect = ConnectionError("refused")
        with patch("core.netbox.get_secret", return_value="token"), \
             patch.dict("sys.modules", {"pynetbox": mock_module}):
            result = load_intent()
        assert result is None
