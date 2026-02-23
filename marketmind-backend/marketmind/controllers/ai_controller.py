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
    user_id = get_jwt_identity()

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
        prompt=prompt_text.strip(),  
        generated_text=caption,
        tone=evaluation["tone"],
        sentiment_score=evaluation["score"]
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
