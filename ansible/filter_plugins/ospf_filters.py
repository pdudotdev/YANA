"""Custom Jinja2 filter plugins for parsing NETCONF XML responses."""
from __future__ import annotations

import xml.etree.ElementTree as ET


def _strip_ns(tag: str) -> str:
    """Strip XML namespace from a tag: '{ns}local' → 'local'."""
    return tag.split("}")[-1] if "}" in tag else tag


def _parse(xml_string: str) -> ET.Element:
    """Parse XML string, handling both raw strings and dict output from netconf_get."""
    if isinstance(xml_string, dict):
        xml_string = xml_string.get("output", "") or xml_string.get("data", "") or str(xml_string)
    try:
        return ET.fromstring(str(xml_string))
    except ET.ParseError:
        return ET.Element("empty")


def route_exists(xml_string: str, prefix: str) -> bool:
    """Return True if a route to the given prefix exists in the routing table.

    Matches if any <destination-prefix> starts with the prefix (e.g. '192.168.42.1'
    matches '192.168.42.1/32'). Works with ietf-routing XML.
    """
    root = _parse(xml_string)
    for elem in root.iter():
        if _strip_ns(elem.tag) == "destination-prefix" and elem.text:
            if elem.text.strip().startswith(prefix):
                return True
    return False


class FilterModule:
    def filters(self) -> dict:
        return {
            "route_exists": route_exists,
        }
