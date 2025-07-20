import os
from dotenv import load_dotenv
from app.app import create_app

load_dotenv()

config = os.getenv("FLASK_ENV") or "development"

app = create_app(config)

if __name__ == "__main__":
    if config == "development":
        app.run(debug=True)
    elif config == "testing":
        from werkzeug.serving import run_simple

        run_simple("0.0.0.0", 5000, app)
