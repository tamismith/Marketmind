from flask import Blueprint, request, jsonify
from ..controllers.ai_controller import (
    generate_ad_copy,
    generate_text_variants,
    select_text_variant,
    get_user_history,
    get_user_analytics,
)
from flask_jwt_extended import jwt_required
from ..responses import error_response


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


@ai_blueprint.route("/ad-copy", methods=["POST"])
@jwt_required()
def ad_copy_endpoint():
    try:
        data = request.get_json(silent=True)

        if not data:
            return error_response(
                "INVALID_REQUEST",
                "Request body must be JSON",
                400,
            )

        missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
        if missing:
            return error_response(
                "MISSING_FIELDS",
                "Required fields are missing",
                400,
                {"missing_fields": missing},
            )

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
        return error_response("GENERATION_ERROR", str(e), 400)
    except Exception as e:
        print("ERROR:", e)
        return error_response(
            "SERVER_ERROR",
            "Something went wrong while generating the ad",
            500,
        )


@ai_blueprint.route("/health", methods=["GET"])
def health_check():
    """
    GET /api/ai/health
    Simple endpoint to confirm AI routes are running
    """
    return jsonify({"status": "ok"}), 200


@ai_blueprint.route("/generate/text", methods=["POST"])
@jwt_required()
def generate_text_endpoint():
    try:
        data = request.get_json(silent=True)
        if not data:
            return error_response(
                "INVALID_REQUEST",
                "Request body must be JSON",
                400,
            )

        missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
        if missing:
            return error_response(
                "MISSING_FIELDS",
                "Required fields are missing",
                400,
                {"missing_fields": missing},
            )

        business_name = data["business_name"].strip()
        industry = data["industry"].strip()
        target_audience = data["target_audience"].strip()
        tone = data["tone"].strip()
        platform = data["platform"].strip()
        description = data["description"].strip()

        goal = (data.get("goal") or "").strip()
        length = (data.get("length") or "short").strip()
        region = (data.get("region") or "UK").strip()

        result = generate_text_variants(
            business_name=business_name,
            industry=industry,
            target_audience=target_audience,
            tone=tone,
            platform=platform,
            description=description,
            goal=goal,
            length=length,
            region=region,
        )

        return jsonify({
            "content_id": result["content_id"],
            "variant_a": result["variant_a"],
            "variant_b": result["variant_b"],
            "evaluation_a": result["evaluation_a"],
            "evaluation_b": result["evaluation_b"],
            "meta": {
                "platform": platform,
                "tone": tone,
                "length": length,
                "region": region,
            },
        }), 200

    except ValueError as e:
        return error_response("GENERATION_ERROR", str(e), 400)
    except Exception:
        return error_response(
            "SERVER_ERROR",
            "Something went wrong while generating text variants",
            500,
        )


@ai_blueprint.route("/select/text", methods=["POST"])
@jwt_required()
def select_text_endpoint():
    try:
        data = request.get_json(silent=True)
        if not data:
            return error_response(
                "INVALID_REQUEST",
                "Request body must be JSON",
                400,
            )

        content_id = data.get("content_id")
        selected_variant = (data.get("selected_variant") or "").strip()

        if content_id is None or not selected_variant:
            return error_response(
                "MISSING_FIELDS",
                "content_id and selected_variant are required",
                400,
                {"missing_fields": ["content_id", "selected_variant"]},
            )

        result = select_text_variant(
            content_id=int(content_id),
            selected_variant=selected_variant,
        )

        return jsonify(result), 200

    except ValueError as e:
        return error_response("VALIDATION_ERROR", str(e), 400)
    except LookupError as e:
        return error_response("NOT_FOUND", str(e), 404)
    except Exception:
        return error_response(
            "SERVER_ERROR",
            "Something went wrong while selecting text variant",
            500,
        )


@ai_blueprint.route("/history", methods=["GET"])
@jwt_required()
def history_endpoint():
    try:
        limit_raw = request.args.get("limit", "20")
        try:
            limit = int(limit_raw)
        except ValueError:
            return error_response(
                "VALIDATION_ERROR",
                "limit must be an integer",
                400,
            )

        result = get_user_history(limit=limit)
        return jsonify(result), 200

    except ValueError as e:
        return error_response("VALIDATION_ERROR", str(e), 400)
    except Exception:
        return error_response(
            "SERVER_ERROR",
            "Something went wrong while fetching history",
            500,
        )


@ai_blueprint.route("/analytics", methods=["GET"])
@jwt_required()
def analytics_endpoint():
    try:
        result = get_user_analytics()
        return jsonify(result), 200
    except Exception:
        return error_response(
            "SERVER_ERROR",
            "Something went wrong while fetching analytics",
            500,
        )
