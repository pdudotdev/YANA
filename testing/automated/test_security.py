"""Security guardrail tests — VRF injection, validation boundaries.

Every injection pattern that must be blocked is tested here in one auditable place.
The regex ^[a-zA-Z0-9_-]{1,32}$ in input_models/models.py is the sole barrier
between user-supplied VRF names and CLI command strings.
"""
import pytest
from pydantic import ValidationError

from input_models.models import OspfQuery, RoutingQuery, TracerouteInput


# ── VRF injection: each pattern MUST be rejected by the Pydantic validator ────

_INJECTION_PATTERNS = [
    "$(reboot)",
    "`reboot`",
    "VRF1|cat /etc/shadow",
    "VRF1\nshow running-config",
    "VRF1\x00cmd",
    "VRF1 extra",
    "VRF1&& rm -rf /",
    "VRF1>/tmp/x",
    "VRF1'",
    'VRF1"',
    "${PATH}",
    "",                 # empty string
    "   ",              # whitespace only
    "VRF1\uff1b",      # fullwidth semicolon U+FF1B
    "VRF1\u2223",      # divides sign U+2223 (pipe look-alike)
    "VRF1;cmd",
    "VRF1\tval",        # tab
    "A" * 33,           # exceeds 32-char limit
]


@pytest.mark.parametrize("bad_vrf", _INJECTION_PATTERNS)
def test_vrf_injection_blocked_ospf(bad_vrf):
    """Every injection payload must raise ValidationError in OspfQuery."""
    with pytest.raises(ValidationError):
        OspfQuery(device="R1", query="neighbors", vrf=bad_vrf)


@pytest.mark.parametrize("bad_vrf", _INJECTION_PATTERNS)
def test_vrf_injection_blocked_routing(bad_vrf):
    """Every injection payload must raise ValidationError in RoutingQuery."""
    with pytest.raises(ValidationError):
        RoutingQuery(device="R1", query="ip_route", vrf=bad_vrf)


@pytest.mark.parametrize("bad_vrf", _INJECTION_PATTERNS)
def test_vrf_injection_blocked_traceroute(bad_vrf):
    """Every injection payload must raise ValidationError in TracerouteInput."""
    with pytest.raises(ValidationError):
        TracerouteInput(device="R1", destination="10.0.0.1", vrf=bad_vrf)


# ── VRF positive cases: valid names MUST be accepted ─────────────────────────

_VALID_VRFS = [
    "VRF1",
    "my_vrf",
    "prod-vrf",
    "A" * 32,           # max length exactly
    "V",                # single character
    "VRF_123-abc",
]


@pytest.mark.parametrize("good_vrf", _VALID_VRFS)
def test_vrf_valid_names_accepted_ospf(good_vrf):
    q = OspfQuery(device="R1", query="neighbors", vrf=good_vrf)
    assert q.vrf == good_vrf


@pytest.mark.parametrize("good_vrf", _VALID_VRFS)
def test_vrf_valid_names_accepted_routing(good_vrf):
    q = RoutingQuery(device="R1", query="ip_route", vrf=good_vrf)
    assert q.vrf == good_vrf


@pytest.mark.parametrize("good_vrf", _VALID_VRFS)
def test_vrf_valid_names_accepted_traceroute(good_vrf):
    q = TracerouteInput(device="R1", destination="10.0.0.1", vrf=good_vrf)
    assert q.vrf == good_vrf
