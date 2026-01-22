from flask import Flask
from flask_cors import CORS
from .config.setting import load_config
from .routes.ai_routes import ai_blueprint

def create_app():
    app = Flask(__name__)

    # Load config (DB URL, etc.)
    load_config(app)

    # Allow React frontend to talk to this API
    CORS(app)

    # Register blueprints (groups of routes)
    app.register_blueprint(ai_blueprint, url_prefix="/api/ai")

    return app
