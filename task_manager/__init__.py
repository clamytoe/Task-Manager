from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # app.config.from_object("config.Config")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ctm.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)

    with app.app_context():
        from . import models, rest_api, routes

        db.create_all()
        app.register_blueprint(routes.routes)

    return app
