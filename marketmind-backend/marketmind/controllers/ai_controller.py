from ..services.ai_service import generate_marketing_text, generate_ad_text
from ..services.evaluation_service import evaluate_text, _calculate_alignment
from ..services.feedback_service import update_brand_memory_from_selection, get_brand_memory, augment_prompt_with_memory
from flask_jwt_extended import get_jwt_identity
from ..models.generated_content import GeneratedContent
from ..models.user import User
from ..models.credit_transaction import CreditTransaction
from ..models.campaign import Campaign
from marketmind.extensions import db

def _campaign_prompt_instruction(name: str, goal: str) -> str:
    if not name or name == "General":
        return ""
    parts = [f"Campaign: {name}"]
    if goal and goal.strip():
        parts.append(f"Campaign goal: {goal.strip()}")
    return "\n".join(parts)


def _vad_prompt_instruction(
    target_valence: float | None,
    target_arousal: float | None,
    target_dominance: float | None,
) -> str:
    """
    Converts numeric VAD targets into a natural-language instruction
    that is appended to the generation prompt so the model actively
    steers toward the desired emotional profile.
    """
    parts = []

    if target_valence is not None:
        if target_valence >= 0.5:
            parts.append("warm, enthusiastic, and positive in tone")
        elif target_valence >= 0.05:
            parts.append("mildly positive and encouraging in tone")
        elif target_valence > -0.05:
            parts.append("neutral and objective in tone")
        elif target_valence > -0.5:
            parts.append("serious or cautious in tone")
        else:
            parts.append("critical and direct in tone")

    if target_arousal is not None:
        if target_arousal >= 0.7:
            parts.append("high-energy and urgent")
        elif target_arousal >= 0.5:
            parts.append("active and engaging")
        elif target_arousal >= 0.3:
            parts.append("moderately energetic")
        else:
            parts.append("calm and measured")

    if target_dominance is not None:
        if target_dominance >= 0.75:
            parts.append("commanding and assertive")
        elif target_dominance >= 0.6:
            parts.append("confident and purposeful")
        elif target_dominance >= 0.4:
            parts.append("balanced and neither passive nor forceful")
        else:
            parts.append("soft and understated")

    if not parts:
        return ""
    return "Emotional target: " + ", ".join(parts) + "."


# Credit cost per action
CREDIT_COST = {
    "text_ab": 2,
    "ad_copy": 5,
    "regenerate": 1,
}


def _check_and_deduct_credits(user_id: int, cost: int, description: str) -> None:
    """
    Raises ValueError if the user has insufficient credits.
    Otherwise deducts and logs the transaction.
    Must be called inside a DB session committed by the caller.
    """
    user = User.query.get(user_id)
    if not user:
        raise LookupError("User not found")
    if user.credits < cost:
        raise ValueError(
            f"Insufficient credits. This action costs {cost} credit(s); "
            f"you have {user.credits}."
        )
    user.credits -= cost
    tx = CreditTransaction(
        user_id=user_id,
        amount=-cost,
        transaction_type="deduction",
        description=description,
    )
    db.session.add(tx)


def generate_ad_copy(
    business_name: str,
    industry: str,
    target_audience: str,
    tone: str,
    platform: str,
    campaign_id: int | None = None,
    description: str = "",
    goal: str = "",
    region: str = "UK",
    length: str = "short",
    offer: str = "",
    cta: str = "",
    color_palette: str = "",
    high_quality: bool = True,
    style_preset: str = "realistic",
    aspect_ratio: str = "1:1",
    shot_type: str = "medium",
    include_keywords="",
    avoid_keywords="",
) -> dict:

    user_id = int(get_jwt_identity())
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=user_id).first() if campaign_id else None
    if campaign_id and not campaign:
        raise LookupError("Campaign not found")

    target_valence = campaign.target_valence if campaign else None
    target_arousal = campaign.target_arousal if campaign else None
    target_dominance = campaign.target_dominance if campaign else None

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
        cta=cta,
        color_palette=color_palette,
        high_quality=high_quality,
        style_preset=style_preset,
        aspect_ratio=aspect_ratio,
        shot_type=shot_type,
        include_keywords=include_keywords,
        avoid_keywords=avoid_keywords,
        vad_instruction=_vad_prompt_instruction(target_valence, target_arousal, target_dominance),
        campaign_instruction=_campaign_prompt_instruction(
            campaign.name if campaign else "",
            campaign.goal if campaign else "",
        ),
    )
    ad_copy = result.get("ad_copy", "")
    if not ad_copy or not ad_copy.strip():
        raise ValueError("AI returned empty output")

    evaluation = evaluate_text(ad_copy)
    alignment = _calculate_alignment(evaluation, target_valence, target_arousal, target_dominance)
    if alignment:
        evaluation["vad_alignment"] = alignment

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
Offer: {offer}
CTA: {cta}
Color palette: {color_palette}
High quality image mode: {"enabled" if high_quality else "disabled"}
Style preset: {style_preset}
Aspect ratio: {aspect_ratio}
Shot type: {shot_type}
Include keywords: {include_keywords}
Avoid keywords: {avoid_keywords}
"""

    _check_and_deduct_credits(user_id, CREDIT_COST["ad_copy"], "Ad copy + image generation")

    content = GeneratedContent(
        user_id=user_id,
        content_type="ad_copy",
        original_prompt=prompt_text.strip(),
        description=description,
        variant_a_text=ad_copy,
        variant_b_text="",
        variant_a_eval_json=evaluation,
        variant_b_eval_json={},
        selected_variant=None,
        campaign_id=campaign_id,
    )
    db.session.add(content)
    db.session.commit()

    result["evaluation"] = evaluation
    result["content_id"] = content.id
    return result


def generate_text_variants(
    business_name: str,
    industry: str,
    target_audience: str,
    platform: str,
    description: str,
    tone: str = "",
    campaign_id: int | None = None,
    goal: str = "",
    region: str = "UK",
    length: str = "short",
) -> dict:
    """
    Generate two distinct text variants, evaluate both, and persist them.
    """
    user_id = int(get_jwt_identity())
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=user_id).first() if campaign_id else None
    if campaign_id and not campaign:
        raise LookupError("Campaign not found")

    target_valence = campaign.target_valence if campaign else None
    target_arousal = campaign.target_arousal if campaign else None
    target_dominance = campaign.target_dominance if campaign else None

    vad_instruction = _vad_prompt_instruction(target_valence, target_arousal, target_dominance)
    # Use tone as fallback only if no VAD targets are set
    effective_tone = tone if not vad_instruction else ""

    memory = get_brand_memory(user_id)
    memory_instruction = augment_prompt_with_memory("", memory) if memory else ""

    angle_a = (
        "Creative brief for Variant A: emotional storytelling. "
        "Start with a relatable moment, paint one vivid scene, and use a warm human voice."
    )
    angle_b = (
        "Creative brief for Variant B: direct performance style. "
        "Lead with concrete value, include one specific benefit, and end with a clear action."
    )

    shared_kwargs = dict(
        business_name=business_name,
        industry=industry,
        target_audience=target_audience,
        tone=effective_tone,
        platform=platform,
        goal=goal,
        length=length,
        region=region,
        vad_instruction=vad_instruction,
        campaign_instruction=_campaign_prompt_instruction(
            campaign.name if campaign else "",
            campaign.goal if campaign else "",
        ) + memory_instruction,
    )

    variant_a = generate_marketing_text(description=f"{description} {angle_a}", **shared_kwargs)
    variant_b = generate_marketing_text(description=f"{description} {angle_b}", **shared_kwargs)

    # If outputs are too close, force a sharper second style split for B.
    if variant_a.strip().lower() == variant_b.strip().lower():
        fallback_b = (
            "Creative brief for Variant B: concise, punchy, and utility-first. "
            "Use different wording from any storytelling style and focus on one measurable outcome."
        )
        variant_b = generate_marketing_text(description=f"{description} {fallback_b}", **shared_kwargs)

    if not variant_a or not variant_a.strip():
        raise ValueError("AI returned empty output for variant A")
    if not variant_b or not variant_b.strip():
        raise ValueError("AI returned empty output for variant B")

    eval_a = evaluate_text(variant_a)
    eval_b = evaluate_text(variant_b)

    alignment_a = _calculate_alignment(eval_a, target_valence, target_arousal, target_dominance)
    alignment_b = _calculate_alignment(eval_b, target_valence, target_arousal, target_dominance)
    if alignment_a:
        eval_a["vad_alignment"] = alignment_a
    if alignment_b:
        eval_b["vad_alignment"] = alignment_b

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

    _check_and_deduct_credits(user_id, CREDIT_COST["text_ab"], "Text A/B generation")

    content = GeneratedContent(
        user_id=user_id,
        content_type="text",
        original_prompt=prompt_text.strip(),
        description=description,
        variant_a_text=variant_a,
        variant_b_text=variant_b,
        variant_a_eval_json=eval_a,
        variant_b_eval_json=eval_b,
        campaign_id=campaign_id,
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


def evaluate_text_only(text: str, campaign_id: int | None = None) -> dict:
    user_id = int(get_jwt_identity())
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=user_id).first() if campaign_id else None
    if campaign_id and not campaign:
        raise LookupError("Campaign not found")

    target_valence = campaign.target_valence if campaign else None
    target_arousal = campaign.target_arousal if campaign else None
    target_dominance = campaign.target_dominance if campaign else None

    evaluation = evaluate_text(text)
    alignment = _calculate_alignment(evaluation, target_valence, target_arousal, target_dominance)
    if alignment:
        evaluation["vad_alignment"] = alignment

    return {
        "evaluation": evaluation,
        "campaign_id": campaign_id,
    }


def _parse_prompt_fields(prompt: str) -> dict:
    """
    Parse all key:value fields from a stored original_prompt string.
    Returns a flat dict with normalised keys (lowercase, spaces → underscores).
    """
    fields: dict = {}
    for line in prompt.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip().lower().replace(" ", "_")] = value.strip()
    return fields


def regenerate_text(content_id: int, instruction: str = "") -> dict:
    """
    Re-generate both A/B text variants for an existing content row.
    Overwrites the row in-place and resets selected_variant.
    Costs 1 credit.
    """
    user_id = int(get_jwt_identity())
    content = GeneratedContent.query.filter_by(id=content_id, user_id=user_id).first()
    if not content:
        raise LookupError("Content not found for this user")
    if content.content_type != "text":
        raise ValueError("Content is not a text generation")

    f = _parse_prompt_fields(content.original_prompt)
    business_name    = f.get("business", "")
    industry         = f.get("industry", "")
    target_audience  = f.get("target_audience", "")
    tone             = f.get("tone", "")
    platform         = f.get("platform", "")
    description      = f.get("description", "")
    goal             = f.get("goal", "")
    length           = f.get("length", "short")
    region           = f.get("region", "UK")

    instruction_line = f"\nUser instruction: {instruction.strip()}" if instruction and instruction.strip() else ""

    angle_a = (
        "Creative brief for Variant A: emotional storytelling. "
        "Start with a relatable moment, paint one vivid scene, and use a warm human voice."
        + instruction_line
    )
    angle_b = (
        "Creative brief for Variant B: direct performance style. "
        "Lead with concrete value, include one specific benefit, and end with a clear action."
        + instruction_line
    )

    memory = get_brand_memory(user_id)
    memory_instruction = augment_prompt_with_memory("", memory) if memory else ""

    shared_kwargs = dict(
        business_name=business_name,
        industry=industry,
        target_audience=target_audience,
        tone=tone,
        platform=platform,
        goal=goal,
        length=length,
        region=region,
        campaign_instruction=memory_instruction,
    )

    variant_a = generate_marketing_text(description=f"{description} {angle_a}", **shared_kwargs)
    variant_b = generate_marketing_text(description=f"{description} {angle_b}", **shared_kwargs)

    if variant_a.strip().lower() == variant_b.strip().lower():
        fallback_b = (
            "Creative brief for Variant B: concise, punchy, and utility-first. "
            "Use different wording from any storytelling style and focus on one measurable outcome."
        )
        variant_b = generate_marketing_text(description=f"{description} {fallback_b}", **shared_kwargs)

    if not variant_a or not variant_a.strip():
        raise ValueError("AI returned empty output for variant A")
    if not variant_b or not variant_b.strip():
        raise ValueError("AI returned empty output for variant B")

    eval_a = evaluate_text(variant_a)
    eval_b = evaluate_text(variant_b)

    _check_and_deduct_credits(user_id, CREDIT_COST["regenerate"], "Text regeneration")

    content.variant_a_text = variant_a
    content.variant_b_text = variant_b
    content.variant_a_eval_json = eval_a
    content.variant_b_eval_json = eval_b
    content.selected_variant = None
    db.session.commit()

    return {
        "content_id": content.id,
        "variant_a": variant_a,
        "variant_b": variant_b,
        "evaluation_a": eval_a,
        "evaluation_b": eval_b,
    }


def regenerate_ad_copy_text(content_id: int) -> dict:
    """
    Re-generate ad copy text for an existing ad_copy row (no image).
    Overwrites the row in-place and resets selected_variant.
    Costs 1 credit.
    """
    user_id = int(get_jwt_identity())
    content = GeneratedContent.query.filter_by(id=content_id, user_id=user_id).first()
    if not content:
        raise LookupError("Content not found for this user")
    if content.content_type != "ad_copy":
        raise ValueError("Content is not an ad copy generation")

    f = _parse_prompt_fields(content.original_prompt)
    business_name   = f.get("business", "")
    industry        = f.get("industry", "")
    target_audience = f.get("target_audience", "")
    tone            = f.get("tone", "")
    platform        = f.get("platform", "")
    description     = f.get("description", "")
    goal            = f.get("goal", "")
    length          = f.get("length", "short")
    region          = f.get("region", "UK")
    offer           = f.get("offer", "")
    cta             = f.get("cta", "")
    color_palette   = f.get("color_palette", "")
    style_preset    = f.get("style_preset", "realistic")
    aspect_ratio    = f.get("aspect_ratio", "1:1")
    shot_type       = f.get("shot_type", "medium")
    include_keywords = f.get("include_keywords", "")
    avoid_keywords   = f.get("avoid_keywords", "")
    high_quality     = f.get("high_quality_image_mode", "enabled") == "enabled"

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
        cta=cta,
        color_palette=color_palette,
        high_quality=high_quality,
        style_preset=style_preset,
        aspect_ratio=aspect_ratio,
        shot_type=shot_type,
        include_keywords=include_keywords,
        avoid_keywords=avoid_keywords,
        text_only=True,
    )

    ad_copy = result.get("ad_copy", "")
    if not ad_copy or not ad_copy.strip():
        raise ValueError("AI returned empty output")

    evaluation = evaluate_text(ad_copy)

    _check_and_deduct_credits(user_id, CREDIT_COST["regenerate"], "Ad copy text regeneration")

    content.variant_a_text = ad_copy
    content.variant_a_eval_json = evaluation
    content.selected_variant = None
    db.session.commit()

    return {
        "content_id": content.id,
        "ad_copy": ad_copy,
        "evaluation": evaluation,
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

    content.selected_variant = selected
    memory_result = update_brand_memory_from_selection(
        user_id=user_id,
        selected_text=selected_text,
    )

    db.session.commit()

    return {
        "content_id": content.id,
        "selected_variant": selected,
        "selected_text": selected_text,
        "brand_memory": memory_result,
    }


def select_ad_image(content_id: int, image_option_id: str, image_base64: str) -> dict:
    if not image_option_id.strip():
        raise ValueError("image_option_id is required")
    if not image_base64.strip():
        raise ValueError("image_base64 is required")

    user_id = int(get_jwt_identity())
    content = GeneratedContent.query.filter_by(id=content_id, user_id=user_id).first()
    if not content:
        raise LookupError("Content not found for this user")
    if content.content_type != "ad_copy":
        raise ValueError("Image selection can only be saved for ad_copy content")

    content.selected_image_option_id = image_option_id.strip()
    content.selected_image_base64 = image_base64.strip()
    db.session.commit()

    return {
        "content_id": content.id,
        "selected_image_option_id": content.selected_image_option_id,
        "saved": True,
    }


def get_user_history(limit: int = 20) -> dict:
    if limit <= 0:
        raise ValueError("limit must be greater than 0")

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

    text_items = []
    ad_copy_items = []
    for row in rows:
        base_item = {
            "content_id": row.id,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "content_type": row.content_type,
            "description": row.description or "",
            "selected_variant": row.selected_variant,
            "selected_image_option_id": row.selected_image_option_id,
            "selected_image_base64": row.selected_image_base64,
            "selected_text": (
                row.variant_a_text if row.selected_variant == "A"
                else row.variant_b_text if row.selected_variant == "B"
                else None
            ),
            "original_prompt": row.original_prompt,
            "variant_a_text": row.variant_a_text,
            "variant_b_text": row.variant_b_text,
            "evaluation_a": row.variant_a_eval_json,
            "evaluation_b": row.variant_b_eval_json,
            "campaign_id": row.campaign_id,
        }
        if row.content_type == "ad_copy":
            ad_copy_items.append({
                **base_item,
                "ad_copy_text": row.variant_a_text,
                "evaluation": row.variant_a_eval_json,
            })
        else:
            text_items.append(base_item)

    return {
        "count": len(rows),
        "text_count": len(text_items),
        "ad_copy_count": len(ad_copy_items),
        "items": text_items,
        "text_items": text_items,
        "ad_copy_items": ad_copy_items,
    }


