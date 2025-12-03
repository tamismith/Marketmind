from flask import Blueprint, request, jsonify
from ..controllers.ai_controller import generate_caption

ai_blueprint = Blueprint("ai", __name__)

@ai_blueprint.route("/caption", methods=["POST"])
def caption_endpoint():
    """
    Expects JSON: { "business_details": "...", "platform": "instagram", ... }
    """
    data = request.get_json()
    result = generate_caption(data)
    return jsonify(result), 200
