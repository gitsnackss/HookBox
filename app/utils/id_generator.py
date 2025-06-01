"""Utility to generate short prefixed IDs."""
import uuid

def generate_id(prefix: str) -> str:
    """Return a unique ID like `wh_abcdef1234`."""
    return f"{prefix}_{uuid.uuid4().hex[:10]}"
