# marketmind/controllers/campaign_controller.py
from collections import Counter
from flask_jwt_extended import get_jwt_identity
from ..models.campaign import Campaign
from ..models.generated_content import GeneratedContent
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


def get_campaign_analytics() -> dict:
    user_id = int(get_jwt_identity())
    campaigns = Campaign.query.filter_by(user_id=user_id).order_by(Campaign.created_at.asc()).all()

    results = []
    for campaign in campaigns:
        rows = GeneratedContent.query.filter_by(user_id=user_id, campaign_id=campaign.id).all()
        selected_rows = [r for r in rows if r.selected_variant in ("A", "B")]

        generation_count = len(rows)
        selection_rate = round(len(selected_rows) / generation_count * 100) if generation_count > 0 else 0

        # Dominant tone from selected eval JSONs
        tones = []
        vad_vals = {"valence": [], "arousal": [], "dominance": []}
        alignment_scores = []
        accuracy_trend = []

        # Sort selected rows oldest-first for the trend chart
        for row in sorted(selected_rows, key=lambda r: r.created_at or 0):
            eval_json = row.variant_a_eval_json if row.selected_variant == "A" else row.variant_b_eval_json
            if not eval_json:
                continue
            tone = eval_json.get("tone")
            if tone:
                tones.append(tone)
            vad = eval_json.get("vad") or {}
            if vad.get("valence") is not None:
                vad_vals["valence"].append(float(vad["valence"]))
            if vad.get("arousal") is not None:
                vad_vals["arousal"].append(float(vad["arousal"]))
            if vad.get("dominance") is not None:
                vad_vals["dominance"].append(float(vad["dominance"]))
            alignment = eval_json.get("vad_alignment") or {}
            if alignment.get("overall") is not None:
                score = float(alignment["overall"])
                alignment_scores.append(score)
                accuracy_trend.append({
                    "date": row.created_at.isoformat() if row.created_at else None,
                    "accuracy": round(score * 100),
                })

        dominant_tone = Counter(tones).most_common(1)[0][0] if tones else None
        avg_vad = {
            "valence": round(sum(vad_vals["valence"]) / len(vad_vals["valence"]), 3) if vad_vals["valence"] else None,
            "arousal": round(sum(vad_vals["arousal"]) / len(vad_vals["arousal"]), 3) if vad_vals["arousal"] else None,
            "dominance": round(sum(vad_vals["dominance"]) / len(vad_vals["dominance"]), 3) if vad_vals["dominance"] else None,
        }
        has_vad_targets = any(x is not None for x in [campaign.target_valence, campaign.target_arousal, campaign.target_dominance])
        brand_language_accuracy = round(sum(alignment_scores) / len(alignment_scores) * 100) if alignment_scores and has_vad_targets else None

        results.append({
            **_serialise(campaign),
            "generation_count": generation_count,
            "selection_rate": selection_rate,
            "dominant_tone": dominant_tone,
            "avg_vad": avg_vad,
            "brand_language_accuracy": brand_language_accuracy,
            "accuracy_trend": accuracy_trend if has_vad_targets else [],
        })

    most_active = max(results, key=lambda x: x["generation_count"], default=None)
    highest_accuracy = max(
        [r for r in results if r["brand_language_accuracy"] is not None],
        key=lambda x: x["brand_language_accuracy"],
        default=None,
    )

    return {
        "campaigns": results,
        "summary": {
            "most_active_campaign": most_active["name"] if most_active else None,
            "highest_accuracy_campaign": highest_accuracy["name"] if highest_accuracy else None,
            "highest_accuracy_value": highest_accuracy["brand_language_accuracy"] if highest_accuracy else None,
        },
    }
