from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.models import User
from App.database import db
from App.models import Exercise

def get_all_exercises():
    exercises = Exercise.query.all()
    return exercises

def get_user_exercises(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    user_exercises = Exercise.query.filter_by(user_id=user.id)
    return user_exercises
