# marketmind/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..responses import error_response

from marketmind.extensions import db
from marketmind.models.user import User

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return error_response(
            "VALIDATION_ERROR",
            "Email and password are required",
            400,
        )

    existing = User.query.filter_by(email=email).first()
    if existing:
        return error_response("CONFLICT", "Email already registered", 409)

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return error_response(
            "VALIDATION_ERROR",
            "Email and password are required",
            400,
        )

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return error_response("UNAUTHORIZED", "Invalid credentials", 401)

    access_token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": access_token}), 200
