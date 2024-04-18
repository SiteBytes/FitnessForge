import os
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from datetime import timedelta
import json


from App.database import init_db
from App.config import config
from App.models.exercises import Exercise
from App.models.user import User


from App.controllers import setup_jwt, add_auth_context

from App.views import views
from App.database import db


def add_views(app):
    for view in views:
        app.register_blueprint(view)


def configure_app(app, config, overrides):
    for key, value in config.items():
        if key in overrides:
            app.config[key] = overrides[key]
        else:
            app.config[key] = config[key]


def create_app(config_overrides={}):
    app = Flask(__name__, static_url_path="/static")
    configure_app(app, config, config_overrides)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config["UPLOADED_PHOTOS_DEST"] = "App/uploads"
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    CORS(app)
    add_auth_context(app)
    photos = UploadSet("photos", TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template("401.html", error=error), 401

    app.app_context().push()
    return app


def initialize_db():
    db.drop_all()
    db.create_all()
    with open("exercises.json", "r", encoding="utf8") as jsonfile:
        data = json.load(jsonfile)
        for row in data:
            exercise = Exercise(
                id=row["id"],
                name=row["name"],
                force=row["force"],
                level=row["level"],
                mechanic=row["mechanic"],
                equipment=row["equipment"],
                primaryMuscles=row["primaryMuscles"],
                secondaryMuscles=row["secondaryMuscles"],
                instructions=row["instructions"],
                category=row["category"],
                images=row["images"],
                )
            db.session.add(exercise)
        bob = User(username="bob", email="bob@mail.com", password="bobpass")
        db.session.add(bob)
        db.session.commit()
