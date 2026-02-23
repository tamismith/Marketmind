from flask import Blueprint, request, jsonify
from ..controllers.ai_controller import generate_caption, generate_ad_copy
from flask_jwt_extended import jwt_required


# Create AI Blueprint
ai_blueprint = Blueprint("ai", __name__)

# Fields that MUST be provided in the request
REQUIRED_FIELDS = [
    "business_name",
    "industry",
    "target_audience",
    "tone",
    "platform",
    "description"
]


@ai_blueprint.route("/caption", methods=["POST"])
@jwt_required()
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
        result = generate_caption(
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
        "caption": result["content"],
        "evaluation": result["evaluation"],
        "meta": {
            "platform": platform,
            "tone": tone,
            "length": length,
            "region": region
        }
    }), 200

    except ValueError as e:
        return jsonify({
            "error": "Generation error",
            "message": str(e)
        }), 400
    except Exception:
        return jsonify({
            "error": "Server error",
            "message": "Something went wrong while generating the caption"
        }), 500



@ai_blueprint.route("/ad-copy", methods=["POST"])
def ad_copy_endpoint():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "Invalid request",
                "message": "Request body must be JSON"
            }), 400

        missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
        if missing:
            return jsonify({
                "error": "Missing fields",
                "missing_fields": missing
            }), 400

        business_name = data["business_name"].strip()
        industry = data["industry"].strip()
        target_audience = data["target_audience"].strip()
        tone = data["tone"].strip()
        platform = data["platform"].strip()
        description = data["description"].strip()

        goal = (data.get("goal") or "").strip()
        length = (data.get("length") or "short").strip()
        region = (data.get("region") or "UK").strip()
        offer = (data.get("offer") or "").strip()
        cta = (data.get("cta") or "").strip()

        result = generate_ad_copy(
            business_name=business_name,
            industry=industry,
            target_audience=target_audience,
            tone=tone,
            platform=platform,
            description=description,
            goal=goal,
            length=length,
            region=region,
            offer=offer,
            cta=cta
        )

        return jsonify({
        "ad_copy": result["ad_copy"],
        "image_base64": result["image_base64"],
        "evaluation": result["evaluation"],
        "meta": {
            "platform": platform,
            "tone": tone,
            "length": length,
            "region": region
        }
    }), 200

    except ValueError as e:
        return jsonify({
            "error": "Generation error",
            "message": str(e)
        }), 400
    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "error": "Server error",
            "message": "Something went wrong while generating the ad"
        }), 500


@ai_blueprint.route("/health", methods=["GET"])
def health_check():
    """
    GET /api/ai/health
    Simple endpoint to confirm AI routes are running
    """
    return jsonify({"status": "ok"}), 200
