import hashlib

def normalize_text(text):
    return " ".join(text.lower().strip().split())

def generate_event_id(text,source):
    """
    Generate deterministic event ID.
    Same logical event => same ID.
    """
    base = f"{source}:{normalize_text(text)}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()