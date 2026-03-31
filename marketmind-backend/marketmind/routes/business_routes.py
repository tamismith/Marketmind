# marketmind/routes/business_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..responses import error_response
from marketmind.controllers.business_controller import get_profile, update_profile

business_blueprint = Blueprint("business", __name__)


@business_blueprint.route("/profile", methods=["GET"])
@jwt_required()
def profile_get():
    user_id = int(get_jwt_identity())
    result = get_profile(user_id)

    if result.get("error") == "NOT_FOUND":
        return error_response("NOT_FOUND", "Business profile not found", 404)

    return jsonify(result), 200


@business_blueprint.route("/profile", methods=["PUT"])
@jwt_required()
def profile_update():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    result = update_profile(user_id, data)

    if result.get("error") == "NOT_FOUND":
        return error_response("NOT_FOUND", "Business profile not found", 404)

    return jsonify(result), 200
