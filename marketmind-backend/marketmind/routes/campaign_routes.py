# marketmind/routes/campaign_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..responses import error_response
from marketmind.controllers.campaign_controller import (
    list_campaigns,
    create_campaign,
    update_campaign,
    delete_campaign,
)

campaign_blueprint = Blueprint("campaigns", __name__)


@campaign_blueprint.route("", methods=["GET"])
@jwt_required()
def campaigns_list():
    try:
        result = list_campaigns()
        return jsonify(result), 200
    except Exception:
        return error_response("SERVER_ERROR", "Something went wrong", 500)


@campaign_blueprint.route("", methods=["POST"])
@jwt_required()
def campaigns_create():
    try:
        data = request.get_json(silent=True) or {}
        result = create_campaign(
            name=data.get("name", ""),
            goal=data.get("goal", ""),
            target_valence=data.get("target_valence"),
            target_arousal=data.get("target_arousal"),
            target_dominance=data.get("target_dominance"),
        )
        return jsonify(result), 201
    except ValueError as e:
        return error_response("VALIDATION_ERROR", str(e), 400)
    except Exception:
        return error_response("SERVER_ERROR", "Something went wrong", 500)


@campaign_blueprint.route("/<int:campaign_id>", methods=["PUT"])
@jwt_required()
def campaigns_update(campaign_id):
    try:
        data = request.get_json(silent=True) or {}
        result = update_campaign(campaign_id, data)
        return jsonify(result), 200
    except ValueError as e:
        return error_response("VALIDATION_ERROR", str(e), 400)
    except LookupError as e:
        return error_response("NOT_FOUND", str(e), 404)
    except Exception:
        return error_response("SERVER_ERROR", "Something went wrong", 500)


@campaign_blueprint.route("/<int:campaign_id>", methods=["DELETE"])
@jwt_required()
def campaigns_delete(campaign_id):
    try:
        result = delete_campaign(campaign_id)
        return jsonify(result), 200
    except ValueError as e:
        return error_response("VALIDATION_ERROR", str(e), 400)
    except LookupError as e:
        return error_response("NOT_FOUND", str(e), 404)
    except Exception:
        return error_response("SERVER_ERROR", "Something went wrong", 500)
