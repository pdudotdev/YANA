# tools package


def _error_response(device: str | None, message: str) -> dict:
    """Return a consistently-shaped error dict for all tool functions."""
    resp = {"error": message}
    if device:
        resp["device"] = device
    return resp
