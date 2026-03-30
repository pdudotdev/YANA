"""UT-006: Ingest helpers — metadata extraction."""
from pathlib import Path

from ingest import extract_metadata


class TestExtractMetadata:
    def test_vendor_file(self):
        meta = extract_metadata(Path("docs/vendor_cisco_ios.md"))
        assert meta["vendor"] == "cisco_ios"
        assert meta["topic"] == "vendor_guide"
        assert meta["source"] == "vendor_cisco_ios.md"
        assert meta["protocol"] == "ospf"

    def test_rfc_file(self):
        meta = extract_metadata(Path("docs/rfc2328_summary.md"))
        assert meta["vendor"] == "all"
        assert meta["topic"] == "rfc"
        assert meta["protocol"] == "ospf"

    def test_rfc3101_protocol(self):
        meta = extract_metadata(Path("docs/rfc3101_nssa.md"))
        assert meta["protocol"] == "ospf"

    def test_unknown_file(self):
        meta = extract_metadata(Path("docs/other.md"))
        assert meta["vendor"] == "all"
        assert meta["topic"] == "general"
        assert meta["protocol"] == "general"

    def test_all_vendor_files(self):
        vendors = ["cisco_ios", "arista_eos", "juniper_junos", "aruba_aoscx", "mikrotik_ros"]
        for v in vendors:
            meta = extract_metadata(Path(f"docs/vendor_{v}.md"))
            assert meta["vendor"] == v
            assert meta["protocol"] == "ospf"

    def test_future_vendor_bgp_file(self):
        """Convention: vendor_<vendor>_<protocol>.md extracts protocol."""
        meta = extract_metadata(Path("docs/vendor_cisco_ios_bgp.md"))
        assert meta["vendor"] == "cisco_ios"
        assert meta["protocol"] == "bgp"
