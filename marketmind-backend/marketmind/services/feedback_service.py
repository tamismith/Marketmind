from typing import Dict, Optional


def get_brand_memory(user_id: int) -> Optional[Dict]:
    """Return structured brand memory for a user, or None if not set."""
    # TODO: load user memory from BrandMemory model once schema is implemented.
    _ = user_id
    return None


def augment_prompt_with_memory(base_prompt: str, brand_memory: Optional[Dict]) -> str:
    """Inject memory-guided style preferences into a prompt safely."""
    # TODO: add deterministic prompt augmentation rules from stored preferences.
    _ = brand_memory
    return base_prompt


def update_brand_memory_from_selection(
    user_id: int,
    selected_text: str,
    context: Dict,
) -> Dict:
    """Update and persist brand memory using selected variant + generation context."""
    # TODO: persist inferred preferences after /select/text is implemented.
    return {
        "user_id": user_id,
        "updated": False,
        "reason": "Brand memory persistence not implemented yet.",
        "selection_preview": selected_text[:120],
        "context_keys": list(context.keys()),
    }
