from ..services.ai_service import create_marketing_caption

def generate_caption(data):
    """
    Controller: validate input, call service, handle errors.
    """
    business_details = data.get("business_details", "")
    platform = data.get("platform", "generic")

    # TODO: add validation, simple rules, etc.
    caption = create_marketing_caption(business_details, platform)

    return {
        "caption": caption
    }
