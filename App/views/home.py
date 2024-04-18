from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from sqlalchemy.exc import IntegrityError

# from App.controllers import 
# from App.database import db
# from App.models import
from datetime import datetime
from App.controllers import get_all_exercises


home_views = Blueprint('home_views', __name__, template_folder='../templates')

@home_views.route('/home', methods=['GET'])
@jwt_required()
def home_page():
    exercises = get_all_exercises()
    return render_template('home.html', exercises=exercises)