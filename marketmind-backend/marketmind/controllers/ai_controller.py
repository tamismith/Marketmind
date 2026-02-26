from ..services.ai_service import generate_marketing_text, generate_ad_text
from ..services.evaluation_service import evaluate_text
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
