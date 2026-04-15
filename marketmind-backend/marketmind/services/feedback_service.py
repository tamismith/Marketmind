from collections import Counter
from typing import Dict, Optional

from marketmind.extensions import db
from marketmind.models.brand_memory import BrandMemory
from marketmind.models.generated_content import GeneratedContent


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
        "preferred_creativity": memory.preferred_creativity if memory.preferred_creativity is not None else 0.5,
    }


def augment_prompt_with_memory(base_prompt: str, brand_memory: Optional[Dict]) -> str:
    """Inject memory-guided style preferences into a prompt safely."""
    if not brand_memory:
        return base_prompt

    memory_lines = []
    if brand_memory.get("preferred_tone"):
        memory_lines.append(f"- Preferred tone: {brand_memory['preferred_tone']}")
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


def update_brand_memory_from_selection(
    user_id: int,
    selected_text: str,
) -> Dict:
    """
    Update and persist brand memory by aggregating across the full selection
    history for this user. Rather than overwriting with the most recent
    selection, memory reflects the dominant pattern across all past choices —
    building a brand language that improves with every interaction.
    """
    memory = BrandMemory.query.filter_by(user_id=user_id).first()
    if not memory:
        memory = BrandMemory(user_id=user_id)
        db.session.add(memory)

    # Fetch all selections this user has ever made, newest first
    rows = (
        GeneratedContent.query
        .filter_by(user_id=user_id)
        .filter(GeneratedContent.selected_variant.isnot(None))
        .order_by(GeneratedContent.created_at.desc())
        .all()
    )

    # --- Tone: most common tone_key across all selected eval JSONs ---
    tones = []
    for row in rows:
        eval_json = (
            row.variant_a_eval_json if row.selected_variant == "A"
            else row.variant_b_eval_json
        )
        tone = (eval_json or {}).get("tone")
        if tone:
            tones.append(tone)

    # --- Platform + Region: most common values from stored prompts ---
    platforms, regions = [], []
    for row in rows:
        for line in (row.original_prompt or "").splitlines():
            if ":" not in line:
                continue
            key, val = line.split(":", 1)
            k = key.strip().lower()
            if k == "platform":
                platforms.append(val.strip())
            elif k == "region":
                regions.append(val.strip())

    # --- Style notes + CTA: derived from 3 most recent selections ---
    recent = rows[:3]
    style_texts, cta_hints = [], []
    for row in recent:
        text = (
            row.variant_a_text if row.selected_variant == "A"
            else row.variant_b_text
        ) or ""
        if text:
            style_texts.append(text[:200])
            hint = _extract_cta_hint(text)
            if hint:
                cta_hints.append(hint)

    # --- Preferred creativity: ratio of A picks to total ---
    a_count = sum(1 for row in rows if row.selected_variant == "A")
    b_count = sum(1 for row in rows if row.selected_variant == "B")
    total = a_count + b_count
    if total > 0:
        memory.preferred_creativity = a_count / total

    # --- Write aggregated memory ---
    if tones:
        memory.preferred_tone = Counter(tones).most_common(1)[0][0]
    if platforms:
        memory.preferred_platform = Counter(platforms).most_common(1)[0][0]
    if regions:
        memory.preferred_region = Counter(regions).most_common(1)[0][0]
    if style_texts:
        memory.style_notes = " | ".join(style_texts)
    if cta_hints:
        memory.cta_preferences = Counter(cta_hints).most_common(1)[0][0]

    return {
        "user_id": user_id,
        "updated": True,
        "reason": "Brand memory aggregated from full selection history.",
        "selection_count": len(rows),
        "dominant_tone": Counter(tones).most_common(1)[0][0] if tones else None,
        "selection_preview": selected_text[:120],
    }
