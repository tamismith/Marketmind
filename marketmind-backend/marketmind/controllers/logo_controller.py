# marketmind/controllers/logo_controller.py
from flask_jwt_extended import get_jwt_identity
from ..services.ai_service import generate_logo_image
from ..models.business_profile import BusinessProfile
from ..models.user import User
from ..models.credit_transaction import CreditTransaction
from marketmind.extensions import db

LOGO_CREDIT_COST = 3


def generate_logo(
    description: str,
    style: str = "minimal",
    feeling: str = "",
    shape: str = "",
    colours: str = "",
) -> dict:
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        raise LookupError("User not found")
    if user.credits < LOGO_CREDIT_COST:
        raise ValueError(
            f"Insufficient credits. Logo generation costs {LOGO_CREDIT_COST} credits; "
            f"you have {user.credits}."
        )

    image_base64 = generate_logo_image(
        description=description,
        style=style,
        feeling=feeling,
        shape=shape,
        colours=colours,
    )
    if not image_base64:
        raise ValueError("Logo generation returned empty result")

    user.credits -= LOGO_CREDIT_COST
    db.session.add(CreditTransaction(
        user_id=user_id,
        amount=-LOGO_CREDIT_COST,
        transaction_type="deduction",
        description="Logo generation",
    ))
    db.session.commit()

    return {"image_base64": image_base64}


def save_logo(image_base64: str) -> dict:
    user_id = int(get_jwt_identity())
    if not image_base64 or not image_base64.strip():
        raise ValueError("image_base64 is required")

    profile = BusinessProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = BusinessProfile(user_id=user_id)
        db.session.add(profile)

    profile.logo_base64 = image_base64.strip()
    db.session.commit()

    return {"saved": True}
