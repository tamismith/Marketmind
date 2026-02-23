from flask import Flask
from flask_cors import CORS
from .config.setting import load_config
from .routes.ai_routes import ai_blueprint
from marketmind.extensions import db, migrate, jwt
from .routes.auth_routes import auth_blueprint
from flask_jwt_extended import JWTManager

jwt = JWTManager()

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

    # Register blueprints (groups of routes)
    app.register_blueprint(ai_blueprint, url_prefix="/api/ai")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")


    return app
