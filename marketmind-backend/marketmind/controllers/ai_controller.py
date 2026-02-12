from ..services.ai_service import generate_marketing_text, generate_ad_text
from ..services.evaluation_service import evaluate_text

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

