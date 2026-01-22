from flask import Blueprint, request, jsonify
from ..controllers.ai_controller import generate_caption

# Create AI Blueprint
ai_blueprint = Blueprint("ai", __name__)

# Fields that MUST be provided in the request
REQUIRED_FIELDS = [
    "business_name",
    "industry",
    "target_audience",
    "tone",
    "platform",
    "description",
    "region"
]


@ai_blueprint.route("/caption", methods=["POST"])
def caption_endpoint():
    """
    POST /api/ai/caption

    Expects JSON:
    {
      "business_name": "Green Brew Cafe",
      "industry": "Coffee shop",
      "target_audience": "Students",
      "tone": "Friendly",
      "platform": "Instagram",
      "description": "Affordable coffee and snacks near campus",
      "goal": "Increase foot traffic",
      "length": "short"
      "region": "UK"

    }

    Returns JSON:
    {
      "caption": "Fuel your study sessions with freshly brewed coffee ☕",
      "meta": {
        "platform": "Instagram",
        "tone": "Friendly",
        "length": "short"
      }
    }
    """
    try:
        # Read JSON body
        data = request.get_json(silent=True)

        # Check JSON exists
        if not data:
            return jsonify({
                "error": "Invalid request",
                "message": "Request body must be JSON"
            }), 400

        # Validate required fields
        missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
        if missing:
            return jsonify({
                "error": "Missing fields",
                "missing_fields": missing
            }), 400

        # Extract required fields
        business_name = data["business_name"].strip()
        industry = data["industry"].strip()
        target_audience = data["target_audience"].strip()
        tone = data["tone"].strip()
        platform = data["platform"].strip()
        description = data["description"].strip()
       

        #  Optional fields (safe defaults)
        goal = (data.get("goal") or "").strip()
        length = (data.get("length") or "short").strip()
        region = (data.get("region") or "UK").strip()

        #  Call controller (controller calls AI service)
        caption = generate_caption(
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

        # Return response
        return jsonify({
            "caption": caption,
            "meta": {
                "platform": platform,
                "tone": tone,
                "length": length
            }
        }), 200

    except Exception:
        return jsonify({
            "error": "Server error",
            "message": "Something went wrong while generating the caption"
        }), 500


@ai_blueprint.route("/health", methods=["GET"])
def health_check():
    """
    GET /api/ai/health
    Simple endpoint to confirm AI routes are running
    """
    return jsonify({"status": "ok"}), 200
