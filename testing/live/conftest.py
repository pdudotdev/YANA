"""Conftest for live tests — --live gate and SSH host key refresh."""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")


def pytest_addoption(parser):
    parser.addoption("--live", action="store_true", default=False, help="Run live device tests")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--live"):
        skip = pytest.mark.skip(reason="Live tests require --live flag")
        for item in items:
            item.add_marker(skip)


@pytest.fixture(scope="session", autouse=True)
def refresh_ssh_host_keys(request):
    """Refresh SSH host keys from lab devices before tests run."""
    if not request.config.getoption("--live"):
        return

    from core.inventory import devices
    if not devices:
        pytest.skip("No devices in inventory")

    hosts = [d["host"] for d in devices.values()]
    known_hosts = Path.home() / ".ssh" / "known_hosts"

    for host in hosts:
        subprocess.run(["ssh-keygen", "-R", host], capture_output=True)

    for host in hosts:
        result = subprocess.run(
            ["ssh-keyscan", "-T", "5", host],
            capture_output=True, text=True,
        )
        if result.stdout.strip():
            with open(known_hosts, "a") as f:
                f.write(result.stdout)
