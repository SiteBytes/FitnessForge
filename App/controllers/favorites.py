from App.models import User, Favorite, Exercise
from App.database import db
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for


def add_favorite(user_id, exercise_id):
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
