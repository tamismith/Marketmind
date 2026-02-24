from flask import Flask
from flask_cors import CORS
from .config.setting import load_config
from .routes.ai_routes import ai_blueprint
from marketmind.extensions import db, migrate, jwt
from .routes.auth_routes import auth_blueprint
from .responses import error_response

def create_app():
    app = Flask(__name__)

    # Load config (DB URL, etc.)
    load_config(app)
    db.init_app(app)  # connect SQLAlchemy to Flask app
    migrate.init_app(app, db)  # enable migrations
    jwt.init_app(app)
    with app.app_context():
        import marketmind.models

    # Allow React frontend to talk to this API
    CORS(app)

    @jwt.unauthorized_loader
    def _unauthorized_loader(reason):
        return error_response(
            "UNAUTHORIZED",
            "Missing or invalid authorization header",
            401,
            {"reason": reason},
        )

    @jwt.invalid_token_loader
    def _invalid_token_loader(reason):
        return error_response(
            "UNAUTHORIZED",
            "Invalid token",
            401,
            {"reason": reason},
        )

    @jwt.expired_token_loader
    def _expired_token_loader(jwt_header, jwt_payload):
        _ = jwt_header
        return error_response(
            "TOKEN_EXPIRED",
            "Access token has expired",
            401,
            {"sub": jwt_payload.get("sub")},
        )

    # Register blueprints (groups of routes)
    app.register_blueprint(ai_blueprint, url_prefix="/api/ai")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")


    return app
