# marketmind/controllers/campaign_controller.py
from flask_jwt_extended import get_jwt_identity
from ..models.campaign import Campaign
from marketmind.extensions import db


def _serialise(c: Campaign) -> dict:
    return {
        "id": c.id,
        "name": c.name,
        "goal": c.goal,
        "target_valence": c.target_valence,
        "target_arousal": c.target_arousal,
        "target_dominance": c.target_dominance,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }


def list_campaigns() -> dict:
    user_id = int(get_jwt_identity())
    campaigns = (
        Campaign.query
        .filter_by(user_id=user_id)
        .order_by(Campaign.created_at.asc())
        .all()
    )
    return {"campaigns": [_serialise(c) for c in campaigns]}


def create_campaign(
    name: str,
    goal: str = "",
    target_valence=None,
    target_arousal=None,
    target_dominance=None,
) -> dict:
    user_id = int(get_jwt_identity())
    if not name or not name.strip():
        raise ValueError("Campaign name is required")

    campaign = Campaign(
        user_id=user_id,
        name=name.strip(),
        goal=goal.strip() if goal else "",
        target_valence=target_valence,
        target_arousal=target_arousal,
        target_dominance=target_dominance,
    )
    db.session.add(campaign)
    db.session.commit()
    return _serialise(campaign)


def update_campaign(campaign_id: int, data: dict) -> dict:
    user_id = int(get_jwt_identity())
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=user_id).first()
    if not campaign:
        raise LookupError("Campaign not found")

    if "name" in data and data["name"].strip():
        campaign.name = data["name"].strip()
    if "goal" in data:
        campaign.goal = (data["goal"] or "").strip()
    if "target_valence" in data:
        campaign.target_valence = data["target_valence"]
    if "target_arousal" in data:
        campaign.target_arousal = data["target_arousal"]
    if "target_dominance" in data:
        campaign.target_dominance = data["target_dominance"]

    db.session.commit()
    return _serialise(campaign)


def delete_campaign(campaign_id: int) -> dict:
    user_id = int(get_jwt_identity())
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=user_id).first()
    if not campaign:
        raise LookupError("Campaign not found")
    if campaign.name == "General":
        raise ValueError("The General campaign cannot be deleted")

    db.session.delete(campaign)
    db.session.commit()
    return {"deleted": True}
