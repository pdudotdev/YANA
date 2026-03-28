"""LT-001: Live platform coverage — all vendors × all OSPF, routing_table, tools + interfaces.

Generates platform_coverage_results.md with detailed output per test.
"""
from datetime import datetime, timezone

import pytest

from core.inventory import devices
from input_models.models import InterfacesQuery, OspfQuery, RoutingQuery, TracerouteInput
from tools.operational import get_interfaces, traceroute
from tools.ospf import get_ospf
from tools.routing import get_routing

# ── Test devices: one per vendor ─────────────────────────────────────────────
TEST_DEVICES = {
    "D1C": "ios",
    "A2A": "eos",
    "C1J": "junos",
    "D2B": "aos",
    "A1M": "routeros",
}

OSPF_QUERIES = ["neighbors", "database", "borders", "config", "interfaces", "details"]
ROUTING_QUERIES = ["ip_route", "route_maps", "prefix_lists", "policy_based_routing", "access_lists"]
TRACEROUTE_DEST = "172.20.20.207"  # C1J management IP — core device reachable from all vendors

RESULTS = []  # collected during test run


# ── Result classification ────────────────────────────────────────────────────
def classify(result: dict) -> str:
    """Classify a tool result as PASS, EMPTY, or FAIL."""
    if "error" in result:
        return "FAIL"
    raw = result.get("raw", "")
    if not raw or not raw.strip():
        return "EMPTY"
    # Vendor-specific empty/error indicators
    stripped = raw.strip()
    if stripped.startswith("% "):
        return "FAIL"
    if stripped.startswith("error:"):
        return "FAIL"
    if "Invalid input" in stripped:
        return "FAIL"
    if "syntax error" in stripped.lower():
        return "FAIL"
    return "PASS"


def record(device: str, category: str, query: str, result: dict, status: str):
    """Record a test result for the markdown report."""
    RESULTS.append({
        "device": device,
        "cli_style": TEST_DEVICES[device],
        "category": category,
        "query": query,
        "status": status,
        "command": result.get("_command", "N/A"),
        "raw": result.get("raw", result.get("error", "no output")),
    })


# ── Markdown report generation ───────────────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def write_results_file(request):
    """Write markdown results after all tests complete."""
    yield  # let all tests run first

    if not RESULTS:
        return

    lines = []
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines.append("# Platform Coverage Results")
    lines.append(f"*Generated: {timestamp}*\n")

    # Summary table
    lines.append("## Summary\n")
    lines.append("| Device | Platform | CLI Style | Tests | Passed | Empty | Failed |")
    lines.append("|--------|----------|-----------|-------|--------|-------|--------|")
    for dev_name, cli_style in TEST_DEVICES.items():
        dev_results = [r for r in RESULTS if r["device"] == dev_name]
        total = len(dev_results)
        passed = sum(1 for r in dev_results if r["status"] == "PASS")
        empty = sum(1 for r in dev_results if r["status"] == "EMPTY")
        failed = sum(1 for r in dev_results if r["status"] == "FAIL")
        platform = devices.get(dev_name, {}).get("platform", "unknown")
        lines.append(f"| {dev_name} | {platform} | {cli_style} | {total} | {passed} | {empty} | {failed} |")

    total_all = len(RESULTS)
    total_pass = sum(1 for r in RESULTS if r["status"] == "PASS")
    total_empty = sum(1 for r in RESULTS if r["status"] == "EMPTY")
    total_fail = sum(1 for r in RESULTS if r["status"] == "FAIL")
    lines.append(f"| **Total** | | | **{total_all}** | **{total_pass}** | **{total_empty}** | **{total_fail}** |")

    # Detailed results per device
    lines.append("\n## Detailed Results\n")
    for dev_name, cli_style in TEST_DEVICES.items():
        platform = devices.get(dev_name, {}).get("platform", "unknown")
        lines.append(f"### {dev_name} — {platform} ({cli_style})\n")
        dev_results = [r for r in RESULTS if r["device"] == dev_name]
        for i, r in enumerate(dev_results, 1):
            lines.append(f"#### {i}. {r['category']} — {r['query']} — {r['status']}")
            lines.append(f"Command: `{r['command']}`")
            # Truncate raw output to 100 lines
            raw_lines = r["raw"].splitlines()
            if len(raw_lines) > 100:
                raw_lines = raw_lines[:100] + [f"... ({len(raw_lines) - 100} more lines truncated)"]
            lines.append("```")
            lines.append("\n".join(raw_lines))
            lines.append("```\n")

    report_path = request.config.rootdir / "testing" / "live" / "platform_coverage_results.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nResults written to {report_path}")


# ── Test cases ───────────────────────────────────────────────────────────────
@pytest.mark.parametrize("device", TEST_DEVICES.keys())
@pytest.mark.parametrize("query", OSPF_QUERIES)
async def test_ospf_query(device, query):
    """Test OSPF query against a live device."""
    result = await get_ospf(OspfQuery(device=device, query=query))
    status = classify(result)
    record(device, "ospf", query, result, status)
    assert status != "FAIL", f"{device} ospf/{query}: {result.get('error', result.get('raw', '')[:200])}"


@pytest.mark.parametrize("device", TEST_DEVICES.keys())
@pytest.mark.parametrize("query", ROUTING_QUERIES)
async def test_routing_query(device, query):
    """Test routing_table query against a live device."""
    result = await get_routing(RoutingQuery(device=device, query=query))
    status = classify(result)
    record(device, "routing_table", query, result, status)
    assert status != "FAIL", f"{device} routing_table/{query}: {result.get('error', result.get('raw', '')[:200])}"


@pytest.mark.parametrize("device", TEST_DEVICES.keys())
async def test_interfaces(device):
    """Test interface status query against a live device."""
    result = await get_interfaces(InterfacesQuery(device=device))
    status = classify(result)
    record(device, "interfaces", "interface_status", result, status)
    assert status != "FAIL", f"{device} interfaces: {result.get('error', result.get('raw', '')[:200])}"


@pytest.mark.parametrize("device", TEST_DEVICES.keys())
async def test_traceroute(device):
    """Test traceroute against a live device, tracing to C1J management IP."""
    result = await traceroute(TracerouteInput(device=device, destination=TRACEROUTE_DEST))
    status = classify(result)
    record(device, "tools", "traceroute", result, status)
    assert status != "FAIL", f"{device} traceroute→{TRACEROUTE_DEST}: {result.get('error', result.get('raw', '')[:200])}"
