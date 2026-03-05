from datetime import date

from ..services.ai_service import generate_marketing_text, generate_ad_text
from ..services.evaluation_service import evaluate_text
from ..services.feedback_service import update_brand_memory_from_selection
from flask_jwt_extended import get_jwt_identity
from ..models.generated_content import GeneratedContent
from marketmind.extensions import db

def generate_caption(
    business_name: str,
    industry: str,
    target_audience: str,
    tone: str,
    platform: str,
    description: str,
    goal: str = "",
    region:str="UK",
    length: str = "short"
) -> dict:
    """
    Controller for AI caption generation.
    Coordinates data between route and service.
    """


    caption = generate_marketing_text(
        business_name=business_name,
        industry=industry,
        target_audience=target_audience,
        tone=tone,
        platform=platform,
        description=description,
        goal=goal,
        length=length,
        region=region
    ) 

    if not caption or not caption.strip():
        raise ValueError("AI returned empty output")
    evaluation = evaluate_text(caption)
    user_id = int(get_jwt_identity())

    prompt_text = f"""
Business: {business_name}
Industry: {industry}
Target Audience: {target_audience}
Tone: {tone}
Platform: {platform}
Description: {description}
Goal: {goal}
Length: {length}
Region: {region}
"""

    # Store in DB
    content = GeneratedContent(
        user_id=user_id,
        original_prompt=prompt_text.strip(),
        # Temporary compatibility write: Week 3 will generate true A/B variants.
        variant_a_text=caption,
        variant_b_text=caption,
        variant_a_eval_json=evaluation,
        variant_b_eval_json=evaluation,
        selected_variant=None,
    )

    db.session.add(content)
    db.session.commit()

    return {
        "content": caption,
        "evaluation": evaluation
    }


def generate_ad_copy(
    business_name: str,
    industry: str,
    target_audience: str,
    tone: str,
    platform: str,
    description: str = "",
    goal: str = "",
    region: str = "UK",
    length: str = "short",
    offer: str = "",
    cta: str = ""
) -> dict:
    
    result = generate_ad_text(
        business_name=business_name,
        industry=industry,
        target_audience=target_audience,
        tone=tone,
        platform=platform,
        description=description,
        goal=goal,
        region=region,
        length=length,
        offer=offer,
        cta=cta
    )
    ad_copy = result.get("ad_copy", "")
    if not ad_copy or not ad_copy.strip():
        raise ValueError("AI returned empty output")

    result["evaluation"] = evaluate_text(ad_copy)
    return result


def generate_text_variants(
    business_name: str,
    industry: str,
    target_audience: str,
    tone: str,
    platform: str,
    description: str,
    goal: str = "",
    region: str = "UK",
    length: str = "short",
) -> dict:
    """
    Generate two distinct text variants, evaluate both, and persist them.
    """
    angle_a = "Creative angle: emotional storytelling with a vivid scene."
    angle_b = "Creative angle: practical value and concrete outcome."

    variant_a = generate_marketing_text(
        business_name=business_name,
        industry=industry,
        target_audience=target_audience,
        tone=tone,
        platform=platform,
        description=f"{description} {angle_a}",
        goal=goal,
        length=length,
        region=region,
    )
    variant_b = generate_marketing_text(
        business_name=business_name,
        industry=industry,
        target_audience=target_audience,
        tone=tone,
        platform=platform,
        description=f"{description} {angle_b}",
        goal=goal,
        length=length,
        region=region,
    )

    if not variant_a or not variant_a.strip():
        raise ValueError("AI returned empty output for variant A")
    if not variant_b or not variant_b.strip():
        raise ValueError("AI returned empty output for variant B")

    eval_a = evaluate_text(variant_a)
    eval_b = evaluate_text(variant_b)
    user_id = int(get_jwt_identity())

    prompt_text = f"""
Business: {business_name}
Industry: {industry}
Target Audience: {target_audience}
Tone: {tone}
Platform: {platform}
Description: {description}
Goal: {goal}
Length: {length}
Region: {region}
"""

    content = GeneratedContent(
        user_id=user_id,
        original_prompt=prompt_text.strip(),
        variant_a_text=variant_a,
        variant_b_text=variant_b,
        variant_a_eval_json=eval_a,
        variant_b_eval_json=eval_b,
        selected_variant=None,
    )
    db.session.add(content)
    db.session.commit()

    return {
        "content_id": content.id,
        "variant_a": variant_a,
        "variant_b": variant_b,
        "evaluation_a": eval_a,
        "evaluation_b": eval_b,
    }


def _extract_context_from_prompt(prompt: str) -> dict:
    context: dict = {}
    for line in prompt.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key_normalized = key.strip().lower().replace(" ", "_")
        context[key_normalized] = value.strip()
    return {
        "tone": context.get("tone", ""),
        "platform": context.get("platform", ""),
        "region": context.get("region", ""),
    }


def select_text_variant(content_id: int, selected_variant: str) -> dict:
    selected = selected_variant.strip().upper()
    if selected not in {"A", "B"}:
        raise ValueError("selected_variant must be 'A' or 'B'")

    user_id = int(get_jwt_identity())
    content = GeneratedContent.query.filter_by(id=content_id, user_id=user_id).first()
    if not content:
        raise LookupError("Content not found for this user")

    selected_text = content.variant_a_text if selected == "A" else content.variant_b_text
    context = _extract_context_from_prompt(content.original_prompt)

    content.selected_variant = selected
    memory_result = update_brand_memory_from_selection(
        user_id=user_id,
        selected_text=selected_text,
        context=context,
    )

    db.session.commit()

    return {
        "content_id": content.id,
        "selected_variant": selected,
        "selected_text": selected_text,
        "brand_memory": memory_result,
    }


def get_user_history(limit: int = 20) -> dict:
    if limit <= 0:
        raise ValueError("limit must be greater than 0")

    # Keep default responses lightweight for frontend usage.
    if limit > 100:
        limit = 100

    user_id = int(get_jwt_identity())
    rows = (
        GeneratedContent.query
        .filter_by(user_id=user_id)
        .order_by(GeneratedContent.created_at.desc())
        .limit(limit)
        .all()
    )

    items = []
    for row in rows:
        items.append({
            "content_id": row.id,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "selected_variant": row.selected_variant,
            "original_prompt": row.original_prompt,
            "variant_a_text": row.variant_a_text,
            "variant_b_text": row.variant_b_text,
            "evaluation_a": row.variant_a_eval_json,
            "evaluation_b": row.variant_b_eval_json,
        })

    return {
        "count": len(items),
        "items": items,
    }


def get_user_analytics() -> dict:
    user_id = int(get_jwt_identity())
    rows = GeneratedContent.query.filter_by(user_id=user_id).all()

    selected_rows = [r for r in rows if (r.selected_variant or "").upper() in {"A", "B"}]

    def selected_eval(row: GeneratedContent) -> dict:
        return row.variant_a_eval_json if row.selected_variant == "A" else row.variant_b_eval_json

    # 1) Best Brand Voice (most common selected tone)
    tone_counts = {"positive": 0, "neutral": 0, "negative": 0}
    for row in selected_rows:
        tone = (selected_eval(row).get("tone") or "neutral").lower()
        if tone not in tone_counts:
            tone = "neutral"
        tone_counts[tone] += 1

    top_tone = max(tone_counts, key=tone_counts.get) if selected_rows else None

    # 2) Weekly Tone Trend (selected tones by ISO week)
    weekly_map = {}
    for row in selected_rows:
        if not row.created_at:
            continue
        iso_year, iso_week, _ = row.created_at.isocalendar()
        week_key = f"{iso_year}-W{iso_week:02d}"
        week_start = date.fromisocalendar(iso_year, iso_week, 1)
        week_end = date.fromisocalendar(iso_year, iso_week, 7)
        week_entry = weekly_map.setdefault(
            week_key,
            {
                "week": week_key,
                "week_start_date": week_start.isoformat(),
                "week_end_date": week_end.isoformat(),
                "positive": 0,
                "neutral": 0,
                "negative": 0,
                "selected_count": 0,
            },
        )
        tone = (selected_eval(row).get("tone") or "neutral").lower()
        if tone not in {"positive", "neutral", "negative"}:
            tone = "neutral"
        week_entry[tone] += 1
        week_entry["selected_count"] += 1

    weekly_tone_trend = [weekly_map[key] for key in sorted(weekly_map.keys())]

    # 3) Regional Style Preference (region counts from selected records)
    region_counts = {}
    for row in selected_rows:
        context = _extract_context_from_prompt(row.original_prompt)
        region = (context.get("region") or "Unknown").strip()
        region_counts[region] = region_counts.get(region, 0) + 1

    regional_style_preference = [
        {"region": region, "selected_count": count}
        for region, count in sorted(region_counts.items(), key=lambda item: item[1], reverse=True)
    ]

    return {
        "best_brand_voice": {
            "top_tone": top_tone,
            "tone_counts": tone_counts,
            "selected_samples": len(selected_rows),
        },
        "weekly_tone_trend": weekly_tone_trend,
        "regional_style_preference": regional_style_preference,
    }
