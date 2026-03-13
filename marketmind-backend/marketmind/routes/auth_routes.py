# marketmind/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..responses import error_response

from marketmind.extensions import db
from marketmind.models.user import User
from marketmind.models.credit_transaction import CreditTransaction

auth_blueprint = Blueprint("auth", __name__)

# ---------------------------------------------------------------------------
# Credit packages available for simulated purchase
# ---------------------------------------------------------------------------
CREDIT_PACKAGES = {
    "topup_100": {
        "label": "Top-up 100 credits",
        "credits": 100,
        "price_display": "£4.99",
        "tier_change": None,
    },
    "starter_monthly": {
        "label": "Starter Plan (monthly)",
        "credits": 200,
        "price_display": "£9.99/mo",
        "tier_change": "starter",
    },
    "pro_monthly": {
        "label": "Pro Plan (monthly)",
        "credits": 600,
        "price_display": "£24.99/mo",
        "tier_change": "pro",
    },
    "enterprise_monthly": {
        "label": "Enterprise Plan (monthly)",
        "credits": 2000,
        "price_display": "£49.99/mo",
        "tier_change": "enterprise",
    },
}


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

    if len(password) < 8:
        return error_response(
            "VALIDATION_ERROR",
            "Password must be at least 8 characters",
            400,
        )

    existing = User.query.filter_by(email=email).first()
    if existing:
        return error_response("CONFLICT", "Email already registered", 409)

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.flush()

    # Log the initial free credit grant
    tx = CreditTransaction(
        user_id=user.id,
        amount=50,
        transaction_type="purchase",
        description="Welcome — free starter credits",
    )
    db.session.add(tx)
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


@auth_blueprint.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return error_response("NOT_FOUND", "User not found", 404)

    return jsonify({
        "email": user.email,
        "credits": user.credits,
        "subscription_tier": user.subscription_tier,
    }), 200


@auth_blueprint.route("/purchase", methods=["POST"])
@jwt_required()
def purchase():
    """Simulated credit purchase — no real payment processed."""
    data = request.get_json(silent=True) or {}
    package_key = (data.get("package") or "").strip()

    package = CREDIT_PACKAGES.get(package_key)
    if not package:
        return error_response(
            "VALIDATION_ERROR",
            "Invalid package. Valid options: " + ", ".join(CREDIT_PACKAGES.keys()),
            400,
        )

    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return error_response("NOT_FOUND", "User not found", 404)

    user.credits += package["credits"]
    if package["tier_change"]:
        user.subscription_tier = package["tier_change"]

    tx = CreditTransaction(
        user_id=user_id,
        amount=package["credits"],
        transaction_type="purchase",
        description=f"Simulated purchase: {package['label']} ({package['price_display']})",
    )
    db.session.add(tx)
    db.session.commit()

    return jsonify({
        "message": f"Purchase successful: {package['label']}",
        "credits_added": package["credits"],
        "credits": user.credits,
        "subscription_tier": user.subscription_tier,
    }), 200


@auth_blueprint.route("/transactions", methods=["GET"])
@jwt_required()
def transactions():
    user_id = int(get_jwt_identity())
    rows = (
        CreditTransaction.query
        .filter_by(user_id=user_id)
        .order_by(CreditTransaction.created_at.desc())
        .limit(50)
        .all()
    )
    return jsonify({
        "transactions": [
            {
                "id": t.id,
                "amount": t.amount,
                "transaction_type": t.transaction_type,
                "description": t.description,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in rows
        ]
    }), 200
