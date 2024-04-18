from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

login_views = Blueprint('login_views', __name__, template_folder='../templates')

@login_views.route('/login', methods=['GET'])
def login_page():
    if not jwt_current_user:
        return render_template('login.html')
    else:
        return redirect(url_for('home_views.home_page'))