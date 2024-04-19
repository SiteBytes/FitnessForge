import os, csv
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
    with open('finalexercises.csv', newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'equipment' in row and row['equipment'] == '':
                row['equipment'] = None
            if 'secondaryMuscles' in row and row['secondaryMuscles'] == '':
                row['secondaryMuscles'] = None
            if 'instructions' in row and row['instructions'] == '':
                row['instructions'] = None
            if 'category' in row and row['category'] == '':
                row['category'] = None
            if 'image1' in row and row['image1'] == '':
                row['image1'] = None
            if 'image2' in row and row['image2'] == '':
                row['image2'] = None
            if 'mechanic' in row and row['mechanic'] == '':
                row['mechanic'] = None

            exercise = Exercise(
            id=row['id'],
            name=row['name'],
            force=row['force'],
            level=row['level'],
            mechanic=row['mechanic'],
            equipment=row['equipment'],
            primaryMuscles=row['primaryMuscles'],
            secondaryMuscles=row['secondaryMuscles'],
            instructions=row['instructions'],
            category=row['category'],
            image1=row['image1'],
            image2=row['image2']
            )
            db.session.add(exercise)
        db.session.commit()
