from marketmind import create_app
from dotenv import load_dotenv
load_dotenv()

app = create_app()

if __name__ == "__main__":
    import os
    app.run(port=5001, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")