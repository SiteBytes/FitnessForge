from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.models import User
from App.database import db
from App.models import Exercise

def get_all_exercises():
    return Exercise.query.all()