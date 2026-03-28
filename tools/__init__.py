# tools package
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
INTENT_JSON = _PROJECT_ROOT / "core" / "legacy" / "INTENT.json"
CHROMA_DIR = _PROJECT_ROOT / "data" / "chroma"


def _error_response(device: str | None, message: str) -> dict:
    """Return a consistently-shaped error dict for all tool functions."""
    resp = {"error": message}
    if device:
        resp["device"] = device
    return resp
