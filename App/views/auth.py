from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, unset_access_cookies, get_jwt_identity, verify_jwt_in_request

from .index import index_views
from flask_jwt_extended.exceptions import NoAuthorizationError

from App.controllers import (
    login,
    create_user,
    get_all_exercises,
    get_all_users
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    

@auth_views.route('/api/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    response = redirect(url_for('home_views.home_page'))
    if not token:
        flash('Bad username or password given'), 401
    else:
        flash('Login Successful')
        set_access_cookies(response, token) 
        return response

# @auth_views.route('/logout', methods=['GET'])
# def logout_action():
#     response = redirect(request.referrer) 
#     flash("Logged Out!")
#     unset_jwt_cookies(response)
#     current_user = None
#     return redirect(url_for('index_views.index_page'))

# @auth_views.route('/logout', methods=['GET'])
# def logout_action():
#     response = redirect(request.referrer) 
#     flash("Logged Out!")
#     unset_jwt_cookies(response)
#     current_user = None
#     return redirect(url_for('index_views.index_page'))

@auth_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form
    user = create_user(data['username'], data['password'])
    if not user:
        flash('Problem Creating New Account'), 401
        return redirect(url_for('auth_views.signup_page'))
    else:
        flash('Sign Up Successful')
        token = login(data['username'], data['password'])
        if not token:
            flash('Bad username or password given'), 401
            return redirect(url_for('auth_views.login_page'))
        else:
            flash('Login Successful')
            response = redirect(url_for('home_views.home_page'))
            set_access_cookies(response, token) 
            return response


@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@auth_views.route('/signup', methods=['GET'])
def signup_page():
    if not current_user:
        return render_template('signup.html')
    else:
        return redirect(url_for('home_views.home_page'))
# '''
# API Routes
# '''

# @auth_views.route('/api/login', methods=['POST'])
# def user_login_api():
#   data = request.json
#   token = login(data['username'], data['password'])
#   if not token:
#     return jsonify(message='bad username or password given'), 401
#   response = jsonify(access_token=token) 
#   set_access_cookies(response, token)
#   return response

# @auth_views.route('/api/identify', methods=['GET'])
# @jwt_required()
# def identify_user():
#     return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = redirect(url_for('index_views.index_page'))
    unset_jwt_cookies(response)
    unset_access_cookies(response)
    return response