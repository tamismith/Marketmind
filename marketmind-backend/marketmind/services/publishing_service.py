from typing import Dict


def export_text_payload(content_id: int, user_id: int) -> Dict:
    """Return export-ready payload (text, metadata, evaluation) for one record."""
    # TODO: fetch content record from DB and enforce user ownership.
    return {
        "content_id": content_id,
        "user_id": user_id,
        "export_ready": False,
        "reason": "Export retrieval not implemented yet.",
    }


def build_channel_export(content: str, channel: str) -> Dict:
    """Format text output for a target channel (e.g., instagram/linkedin)."""
    normalized_channel = (channel or "").strip().lower()

    # TODO: apply channel-specific formatting once publishing flow is implemented.
    return {
        "channel": normalized_channel or "generic",
        "content": content.strip(),
        "formatted": False,
    }
