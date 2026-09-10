import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)

    # Default config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///ctm.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    # Test overrides
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()
        app.register_blueprint(routes.routes)

    return app
