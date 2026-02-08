import os
from dotenv import load_dotenv

load_dotenv()

def load_config(app):
    app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    
