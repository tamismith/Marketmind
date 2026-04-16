import logging
from flask import Blueprint, request, jsonify

logger = logging.getLogger(__name__)
from ..controllers.ai_controller import (
    generate_ad_copy,
    generate_text_variants,
    regenerate_text,
    regenerate_ad_copy_text,
    select_text_variant,
    select_ad_image,
    get_user_history,
    evaluate_text_only,
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
    "platform",
    "description"
]

ALLOWED_STYLE_PRESETS = {"realistic", "bold", "minimal", "warm"}
ALLOWED_ASPECT_RATIOS = {"1:1", "4:5", "16:9"}
ALLOWED_SHOT_TYPES = {"close_up", "medium", "wide"}

def _to_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


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
        tone = (data.get("tone") or "").strip()
        platform = data["platform"].strip()
        description = data["description"].strip()

        goal = (data.get("goal") or "").strip()
        length = (data.get("length") or "short").strip()
        region = (data.get("region") or "UK").strip()
        offer = (data.get("offer") or "").strip()
        cta = (data.get("cta") or "").strip()
        color_palette = (data.get("color_palette") or "").strip()
        high_quality = _to_bool(data.get("high_quality", True))
        style_preset = (data.get("style_preset") or "realistic").strip().lower()
        aspect_ratio = (data.get("aspect_ratio") or "1:1").strip()
        shot_type = (data.get("shot_type") or "medium").strip().lower()
        include_keywords = data.get("include_keywords") or ""
        avoid_keywords = data.get("avoid_keywords") or ""
        campaign_id = data.get("campaign_id")

        if style_preset not in ALLOWED_STYLE_PRESETS:
            return error_response(
                "VALIDATION_ERROR",
                "Invalid style_preset",
                400,
                {"allowed_values": sorted(ALLOWED_STYLE_PRESETS)},
            )
        if aspect_ratio not in ALLOWED_ASPECT_RATIOS:
            return error_response(
                "VALIDATION_ERROR",
                "Invalid aspect_ratio",
                400,
                {"allowed_values": sorted(ALLOWED_ASPECT_RATIOS)},
            )
        if shot_type not in ALLOWED_SHOT_TYPES:
            return error_response(
                "VALIDATION_ERROR",
                "Invalid shot_type",
                400,
                {"allowed_values": sorted(ALLOWED_SHOT_TYPES)},
            )

        result = generate_ad_copy(
            business_name=business_name,
            industry=industry,
            target_audience=target_audience,
            tone=tone,
            platform=platform,
            campaign_id=campaign_id,
            description=description,
            goal=goal,
            length=length,
            region=region,
            offer=offer,
            cta=cta,
            color_palette=color_palette,
            high_quality=high_quality,
            style_preset=style_preset,
            aspect_ratio=aspect_ratio,
            shot_type=shot_type,
            include_keywords=include_keywords,
            avoid_keywords=avoid_keywords,
        )

        return jsonify({
        "content_id": result["content_id"],
        "ad_copy": result["ad_copy"],
        "image_base64": result["image_base64"],
        "image_options": result.get("image_options", []),
        "image_warnings": result.get("image_warnings", []),
        "evaluation": result["evaluation"],
        "meta": {
            "platform": platform,
            "tone": tone,
            "length": length,
            "region": region,
            "color_palette": color_palette,
            "high_quality": high_quality,
            "style_preset": style_preset,
            "aspect_ratio": aspect_ratio,
            "shot_type": shot_type,
        }
    }), 200

    except ValueError as e:
        msg = str(e)
        if "Insufficient credits" in msg:
            return error_response("INSUFFICIENT_CREDITS", msg, 402)
        return error_response("GENERATION_ERROR", msg, 400)
    except Exception as e:
        logger.error("ERROR: %s", e)
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
        tone = (data.get("tone") or "").strip()
        platform = data["platform"].strip()
        description = data["description"].strip()

        goal = (data.get("goal") or "").strip()
        length = (data.get("length") or "short").strip()
        region = (data.get("region") or "UK").strip()
        campaign_id = data.get("campaign_id")
        generation_mode = (data.get("generation_mode") or "vad_driven").strip()

        result = generate_text_variants(
            business_name=business_name,
            industry=industry,
            target_audience=target_audience,
            tone=tone,
            platform=platform,
            description=description,
            campaign_id=campaign_id,
            goal=goal,
            length=length,
            region=region,
            generation_mode=generation_mode,
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
        msg = str(e)
        if "Insufficient credits" in msg:
            return error_response("INSUFFICIENT_CREDITS", msg, 402)
        return error_response("GENERATION_ERROR", msg, 400)
    except Exception:
        return error_response(
            "SERVER_ERROR",
            "Something went wrong while generating text variants",
            500,
        )


@ai_blueprint.route("/regenerate/text", methods=["POST"])
@jwt_required()
def regenerate_text_endpoint():
    try:
        data = request.get_json(silent=True)
        if not data:
            return error_response("INVALID_REQUEST", "Request body must be JSON", 400)

        content_id = data.get("content_id")
        if content_id is None:
            return error_response(
                "MISSING_FIELDS",
                "content_id is required",
                400,
                {"missing_fields": ["content_id"]},
            )

        instruction = data.get("instruction", "")
        result = regenerate_text(content_id=int(content_id), instruction=instruction)
        return jsonify(result), 200

    except ValueError as e:
        msg = str(e)
        if "Insufficient credits" in msg:
            return error_response("INSUFFICIENT_CREDITS", msg, 402)
        return error_response("GENERATION_ERROR", msg, 400)
    except LookupError as e:
        return error_response("NOT_FOUND", str(e), 404)
    except Exception as e:
        logger.error("ERROR: %s", e)
        return error_response("SERVER_ERROR", "Something went wrong while regenerating text", 500)


@ai_blueprint.route("/regenerate/ad-copy", methods=["POST"])
@jwt_required()
def regenerate_ad_copy_endpoint():
    try:
        data = request.get_json(silent=True)
        if not data:
            return error_response("INVALID_REQUEST", "Request body must be JSON", 400)

        content_id = data.get("content_id")
        if content_id is None:
            return error_response(
                "MISSING_FIELDS",
                "content_id is required",
                400,
                {"missing_fields": ["content_id"]},
            )

        result = regenerate_ad_copy_text(content_id=int(content_id))
        return jsonify(result), 200

    except ValueError as e:
        msg = str(e)
        if "Insufficient credits" in msg:
            return error_response("INSUFFICIENT_CREDITS", msg, 402)
        return error_response("GENERATION_ERROR", msg, 400)
    except LookupError as e:
        return error_response("NOT_FOUND", str(e), 404)
    except Exception as e:
        logger.error("ERROR: %s", e)
        return error_response("SERVER_ERROR", "Something went wrong while regenerating ad copy", 500)


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


@ai_blueprint.route("/select/ad-image", methods=["POST"])
@jwt_required()
def select_ad_image_endpoint():
    try:
        data = request.get_json(silent=True)
        if not data:
            return error_response(
                "INVALID_REQUEST",
                "Request body must be JSON",
                400,
            )

        content_id = data.get("content_id")
        image_option_id = (data.get("image_option_id") or "").strip()
        image_base64 = (data.get("image_base64") or "").strip()

        if content_id is None or not image_option_id or not image_base64:
            return error_response(
                "MISSING_FIELDS",
                "content_id, image_option_id, and image_base64 are required",
                400,
                {"missing_fields": ["content_id", "image_option_id", "image_base64"]},
            )

        result = select_ad_image(
            content_id=int(content_id),
            image_option_id=image_option_id,
            image_base64=image_base64,
        )
        return jsonify(result), 200

    except ValueError as e:
        return error_response("VALIDATION_ERROR", str(e), 400)
    except LookupError as e:
        return error_response("NOT_FOUND", str(e), 404)
    except Exception:
        return error_response(
            "SERVER_ERROR",
            "Something went wrong while saving ad image selection",
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


@ai_blueprint.route("/evaluate", methods=["POST"])
@jwt_required()
def evaluate_endpoint():
    try:
        data = request.get_json(silent=True)
        if not data:
            return error_response("INVALID_REQUEST", "Request body must be JSON", 400)

        text = (data.get("text") or "").strip()
        campaign_id = data.get("campaign_id")

        if not text:
            return error_response("MISSING_FIELDS", "text is required", 400)

        result = evaluate_text_only(text=text, campaign_id=campaign_id)
        return jsonify(result), 200

    except LookupError as e:
        return error_response("NOT_FOUND", str(e), 404)
    except Exception as e:
        logger.error("EVALUATE ERROR: %s", e)
        return error_response("SERVER_ERROR", "Something went wrong during evaluation", 500)


