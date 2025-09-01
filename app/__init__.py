from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__, static_folder="../static")
    app.config.from_object("config.Config")

    CORS(app)

    from .api import api_bp
    from .static import static_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(static_bp)

    return app
