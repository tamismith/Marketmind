# marketmind/routes/logo_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..responses import error_response
from marketmind.controllers.logo_controller import generate_logo, save_logo

logo_blueprint = Blueprint("logo", __name__)


@logo_blueprint.route("/generate", methods=["POST"])
@jwt_required()
def logo_generate():
    try:
        data = request.get_json(silent=True) or {}
        description = (data.get("description") or "").strip()
        style = (data.get("style") or "minimal").strip()
        feeling = (data.get("feeling") or "").strip()
        shape = (data.get("shape") or "").strip()
        colours = (data.get("colours") or "").strip()

        if not description:
            return error_response("MISSING_FIELDS", "description is required", 400)

        result = generate_logo(
            description=description,
            style=style,
            feeling=feeling,
            shape=shape,
            colours=colours,
        )
        return jsonify(result), 200

    except ValueError as e:
        msg = str(e)
        if "Insufficient credits" in msg:
            return error_response("INSUFFICIENT_CREDITS", msg, 402)
        return error_response("GENERATION_ERROR", msg, 400)
    except LookupError as e:
        return error_response("NOT_FOUND", str(e), 404)
    except Exception:
        return error_response("SERVER_ERROR", "Something went wrong during logo generation", 500)


@logo_blueprint.route("/save", methods=["POST"])
@jwt_required()
def logo_save():
    try:
        data = request.get_json(silent=True) or {}
        image_base64 = (data.get("image_base64") or "").strip()

        if not image_base64:
            return error_response("MISSING_FIELDS", "image_base64 is required", 400)

        result = save_logo(image_base64=image_base64)
        return jsonify(result), 200

    except ValueError as e:
        return error_response("VALIDATION_ERROR", str(e), 400)
    except LookupError as e:
        return error_response("NOT_FOUND", str(e), 404)
    except Exception:
        return error_response("SERVER_ERROR", "Something went wrong while saving logo", 500)
