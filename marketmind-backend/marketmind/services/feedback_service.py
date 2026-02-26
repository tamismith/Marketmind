from typing import Dict, Optional

from marketmind.extensions import db
from marketmind.models.brand_memory import BrandMemory


def get_brand_memory(user_id: int) -> Optional[Dict]:
    """Return structured brand memory for a user, or None if not set."""
    memory = BrandMemory.query.filter_by(user_id=user_id).first()
    if not memory:
        return None
    return {
        "preferred_tone": memory.preferred_tone,
        "preferred_platform": memory.preferred_platform,
        "preferred_region": memory.preferred_region,
        "style_notes": memory.style_notes,
        "cta_preferences": memory.cta_preferences,
    }


def augment_prompt_with_memory(base_prompt: str, brand_memory: Optional[Dict]) -> str:
    """Inject memory-guided style preferences into a prompt safely."""
    if not brand_memory:
        return base_prompt

    memory_lines = []
    if brand_memory.get("preferred_tone"):
        memory_lines.append(f"- Preferred tone: {brand_memory['preferred_tone']}")
    if brand_memory.get("preferred_platform"):
        memory_lines.append(f"- Preferred platform style: {brand_memory['preferred_platform']}")
    if brand_memory.get("preferred_region"):
        memory_lines.append(f"- Preferred region style: {brand_memory['preferred_region']}")
    if brand_memory.get("style_notes"):
        memory_lines.append(f"- Style notes: {brand_memory['style_notes']}")
    if brand_memory.get("cta_preferences"):
        memory_lines.append(f"- CTA preference: {brand_memory['cta_preferences']}")

    if not memory_lines:
        return base_prompt

    memory_block = "\n".join(memory_lines)
    return f"{base_prompt}\n\nBRAND MEMORY HINTS:\n{memory_block}"


def _extract_cta_hint(selected_text: str) -> str:
    parts = [p.strip() for p in selected_text.replace("?", ".").split(".") if p.strip()]
    if not parts:
        return ""
    last = parts[-1]
    if len(last) > 120:
        return last[:120]
    return last
    return base_prompt


def update_brand_memory_from_selection(
    user_id: int,
    selected_text: str,
    context: Dict,
) -> Dict:
    """Update and persist brand memory using selected variant + generation context."""
    memory = BrandMemory.query.filter_by(user_id=user_id).first()
    if not memory:
        memory = BrandMemory(user_id=user_id)
        db.session.add(memory)

    tone = (context.get("tone") or "").strip() or None
    platform = (context.get("platform") or "").strip() or None
    region = (context.get("region") or "").strip() or None

    if tone:
        memory.preferred_tone = tone
    if platform:
        memory.preferred_platform = platform
    if region:
        memory.preferred_region = region

    memory.style_notes = selected_text[:400]
    cta_hint = _extract_cta_hint(selected_text)
    if cta_hint:
        memory.cta_preferences = cta_hint

    return {
        "user_id": user_id,
        "updated": True,
        "reason": "Brand memory updated from selected variant.",
        "selection_preview": selected_text[:120],
        "context_keys": list(context.keys()),
    }
