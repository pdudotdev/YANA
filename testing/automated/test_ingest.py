"""UT-006: Ingest helpers — metadata extraction and markdown conversion."""
from pathlib import Path


from ingest import _router_to_markdown, extract_metadata


class TestExtractMetadata:
    def test_vendor_file(self):
        meta = extract_metadata(Path("docs/vendor_cisco_ios.md"))
        assert meta["vendor"] == "cisco_ios"
        assert meta["topic"] == "vendor_guide"
        assert meta["source"] == "vendor_cisco_ios.md"

    def test_rfc_file(self):
        meta = extract_metadata(Path("docs/rfc2328_summary.md"))
        assert meta["vendor"] == "all"
        assert meta["topic"] == "rfc"

    def test_rfc3101(self):
        meta = extract_metadata(Path("docs/rfc3101_nssa.md"))
        assert meta["vendor"] == "all"
        assert meta["topic"] == "rfc"

    def test_unknown_file(self):
        meta = extract_metadata(Path("docs/other.md"))
        assert meta["vendor"] == "all"
        assert meta["topic"] == "general"

    def test_all_vendor_files(self):
        vendors = ["cisco_ios", "arista_eos", "juniper_junos", "aruba_aoscx", "mikrotik_ros"]
        for v in vendors:
            meta = extract_metadata(Path(f"docs/vendor_{v}.md"))
            assert meta["vendor"] == v


class TestRouterToMarkdown:
    def test_basic_router(self):
        router = {
            "roles": ["ABR", "OSPF_AREA0_DISTRIBUTION"],
            "platform": "cisco_iosxe",
            "vrf": "VRF1",
            "igp": {
                "ospf": {
                    "router_id": "11.11.11.11",
                    "areas": {"0": ["10.0.0.0/30"], "1": ["10.1.1.0/30"]},
                    "area_types": {"1": "stub"},
                }
            },
            "direct_links": {
                "A1M": {"local_interface": "Ethernet0/1", "local_ip": "10.1.1.2"},
            },
        }
        md = _router_to_markdown("D1C", router)
        assert "## D1C" in md
        assert "ABR" in md
        assert "11.11.11.11" in md
        assert "Area 0 normal" in md
        assert "Area 1 stub" in md
        assert "A1M (Ethernet0/1, 10.1.1.2)" in md

    def test_router_with_bgp(self):
        router = {
            "roles": ["ASBR"],
            "platform": "cisco_iosxe",
            "asn": 1010,
            "bgp": {
                "neighbors": {
                    "ISP_A": {"as": 4040, "peer": "200.40.40.2"},
                }
            },
        }
        md = _router_to_markdown("E1C", router)
        assert "BGP AS: 1010" in md
        assert "ISP_A (AS 4040, 200.40.40.2)" in md

    def test_router_minimal(self):
        router = {"roles": ["LEAF"], "platform": "arista_eos"}
        md = _router_to_markdown("A2A", router)
        assert "## A2A" in md
        assert "LEAF" in md
