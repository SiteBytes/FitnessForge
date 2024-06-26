from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy.exc import IntegrityError
import os

from sqlalchemy import or_

from App.database import db
from App.controllers import get_all_exercises, add_favorite, delete_favorite
from App.models import Exercise, Favorite


home_views = Blueprint('home_views', __name__, template_folder='../templates')
imagekit_url_endpoint = os.getenv('IMAGEKIT_URL_ENDPOINT')
# @home_views.route('/home', methods=['GET'])
# @jwt_required()
# def home_page():
#     exercises = Exercise.query.all()
#     favorites = Favorite.query.filter_by(user=current_user).all()
#     imagekit_url_endpoint = os.getenv('IMAGEKIT_URL_ENDPOINT')
#     return render_template('home.html', exercises=exercises, favorites=favorites, imagekit_url_endpoint=imagekit_url_endpoint)
@home_views.route('/home')
@jwt_required()
def home_page():
    page = request.args.get('page', 1, type=int)
    exercises = Exercise.query.paginate(page=page, per_page=10, error_out=False).items
    favorites = Favorite.query.filter_by(user=current_user).all()
    return render_template('home.html', exercises=exercises, favorites=favorites, imagekit_url_endpoint=imagekit_url_endpoint)

@home_views.route('/search', methods=['GET'])
@jwt_required()
def search():
    query = request.args.get('query')
    exercises = Exercise.query.filter(or_(Exercise.name.contains(query), Exercise.instructions.contains(query))).all()
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', exercises=exercises, favorites=favorites, imagekit_url_endpoint=imagekit_url_endpoint)

@home_views.route('/add-favorite', methods=['POST'])
@jwt_required()
def add_favorite():
    exercise_id = request.form['exercise_id']
    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        flash('Exercise not found', 'error')
        return redirect(url_for('home_views.home_page'))
    try:
        favorite = Favorite(exercise=exercise, user=current_user)
        db.session.add(favorite)
        db.session.commit()
        flash('Favorite added', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Favorite already added', 'error')
    exercises = Exercise.query.all()
    favorites = Favorite.query.filter_by(user=current_user).all()
    return redirect(url_for('home_views.home_page'))

@home_views.route('/delete-favorite', methods=['POST'])
@jwt_required()
def delete_favorite():
    exercise_id = request.form['exercise_id']
    favorite_exercise = Favorite.query.filter_by(exercise_id=exercise_id, user_id=current_user.id).first()
    
    if favorite_exercise:
        try:
            db.session.delete(favorite_exercise)
            db.session.commit()
            flash('Favorite removed', 'successs')
        
        except IntegrityError:
            db.session.rollback()
            flash ('Error removing favorite', 'error')
            flash('Favorite not found', 'error')
        exercises= Exercise.query.all()
        favorites= Favorite.query.filter_by(user_id=current_user.id).all()
        return redirect(url_for('home_views.home_page'))


@home_views.route('/api/exercises', methods=['GET'])
@jwt_required()
def get_exercises():
    page = request.args.get('page', 1, type=int)
    PER_PAGE = 10
    exercises = Exercise.query.paginate(page, PER_PAGE, False).items
    return jsonify([exercise.serialize() for exercise in exercises])