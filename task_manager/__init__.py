import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)

    # Default DB (production)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///ctm.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    # Apply test overrides
    if test_config:
        app.config.update(test_config)

    # Safety guard: never allow tests to use the production DB
    uri = app.config["SQLALCHEMY_DATABASE_URI"]
    if app.config.get("TESTING") and "ctm.db" in uri:
        raise RuntimeError(
            "Refusing to run tests against production database (ctm.db). "
            "Tests must use a temporary SQLite file."
        )
    if app.config.get("TESTING") and "dev.db" in uri:
        raise RuntimeError("Tests cannot use dev.db either.")

    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()
        app.register_blueprint(routes.routes)

    return app
