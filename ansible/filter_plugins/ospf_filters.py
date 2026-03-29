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

    Handles two XML formats:
      - ietf-routing: matches <destination-prefix> (IOS-XE)
      - JunOS RPC: matches <rt-destination> (get-route-information)
    Matches if any element starts with the prefix (e.g. '192.168.42.1'
    matches '192.168.42.1/32').
    """
    root = _parse(xml_string)
    match_tags = {"destination-prefix", "rt-destination"}
    for elem in root.iter():
        if _strip_ns(elem.tag) in match_tags and elem.text:
            if elem.text.strip().startswith(prefix):
                return True
    return False


def ospf_neighbor_full(xml_string: str, neighbor_id: str) -> bool:
    """Return True if a neighbor with the given router-id is in FULL state.

    Finds the neighbor ID in the XML, then checks sibling elements for a
    'full' state string. Works with Cisco-IOS-XE-ospf-oper YANG output.
    """
    root = _parse(xml_string)
    parent_map = {c: p for p in root.iter() for c in p}
    for elem in root.iter():
        if elem.text and elem.text.strip() == neighbor_id:
            parent = parent_map.get(elem)
            if parent is not None:
                for sibling in parent:
                    if sibling.text and "full" in sibling.text.strip().lower():
                        return True
    return False


def config_contains(xml_string: str, value: str) -> bool:
    """Return True if any element's text matches the given value exactly.

    Used for checking configuration elements (e.g. route-map names) in
    NETCONF running config responses.
    """
    root = _parse(xml_string)
    for elem in root.iter():
        if elem.text and elem.text.strip() == value:
            return True
    return False


def assert_check(xml_string: str, assertion: str, value: str) -> bool:
    """Dispatch to the appropriate assertion function by name."""
    checks = {
        "route_exists": route_exists,
        "ospf_neighbor_full": ospf_neighbor_full,
        "config_contains": config_contains,
    }
    fn = checks.get(assertion)
    if fn is None:
        raise ValueError(f"Unknown assertion type: {assertion}")
    return fn(xml_string, value)


class FilterModule:
    def filters(self) -> dict:
        return {
            "route_exists": route_exists,
            "ospf_neighbor_full": ospf_neighbor_full,
            "config_contains": config_contains,
            "assert_check": assert_check,
        }
