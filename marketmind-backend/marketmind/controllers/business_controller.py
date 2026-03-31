# marketmind/controllers/business_controller.py
from marketmind.extensions import db
from marketmind.models.business_profile import BusinessProfile


def get_profile(user_id: int) -> dict:
    profile = BusinessProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return {"error": "NOT_FOUND"}

    return {
        "business_name": profile.business_name,
        "industry": profile.industry,
        "target_audience": profile.target_audience,
        "region": profile.region,
        "logo_base64": profile.logo_base64,
        "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
    }


def update_profile(user_id: int, data: dict) -> dict:
    profile = BusinessProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return {"error": "NOT_FOUND"}

    allowed_fields = ["business_name", "industry", "target_audience", "region", "logo_base64"]

    for field in allowed_fields:
        if field in data:
            setattr(profile, field, data[field])

    db.session.commit()

    return {
        "business_name": profile.business_name,
        "industry": profile.industry,
        "target_audience": profile.target_audience,
        "region": profile.region,
        "logo_base64": profile.logo_base64,
        "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
    }
