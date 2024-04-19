from App.models import User, Favorite, Exercise
from App.database import db
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for


def create_user(username, password):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user is not None:
        return "User with this username already exists"
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None


def save_favorite(user_id, exercise_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        return jsonify({'error': 'Exercise not found'}), 404
    favorite = Favorite(user_id=user.id, exercise_id=exercise.id)
    db.session.add(favorite)
    db.session.commit()
    return favorite.get_json()

def delete_favorite(user_id, exercise_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        return jsonify({'error': 'Exercise not found'}), 404
    favorite = Favorite.query.filter_by(user_id=user.id, exercise_id=exercise.id).first()
    if favorite is None:
        return jsonify({'error': 'Favorite not found'}), 404
    db.session.delete(favorite)
    db.session.commit()
    return favorite.get_json()
