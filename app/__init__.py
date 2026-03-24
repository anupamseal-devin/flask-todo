import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(testing=False):
    """Application factory for creating the Flask app."""
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "DATABASE_URI", "sqlite:///db.sqlite"
        )

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes.api import api_bp
    from app.routes.views import views_bp

    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Create database tables
    with app.app_context():
        from app.models.todo import Todo  # noqa: F401

        db.create_all()

    return app
