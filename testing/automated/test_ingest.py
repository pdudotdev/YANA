"""UT-006: Ingest helpers — metadata extraction."""
from pathlib import Path

from ingest import extract_metadata


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

    def test_unknown_file(self):
        meta = extract_metadata(Path("docs/other.md"))
        assert meta["vendor"] == "all"
        assert meta["topic"] == "general"

    def test_all_vendor_files(self):
        vendors = ["cisco_ios", "arista_eos", "juniper_junos", "aruba_aoscx", "mikrotik_ros"]
        for v in vendors:
            meta = extract_metadata(Path(f"docs/vendor_{v}.md"))
            assert meta["vendor"] == v
