from ..services.ai_service import generate_marketing_text


def generate_caption(
    business_name: str,
    industry: str,
    target_audience: str,
    tone: str,
    platform: str,
    description: str,
    goal: str = "",
    region:str="",
    length: str = "short"
) -> str:
    """
    Controller for AI caption generation.
    Coordinates data between route and service.
    """

    return generate_marketing_text(
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
