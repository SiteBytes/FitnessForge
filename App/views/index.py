from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from flask_jwt_extended import jwt_required, current_user
from App.models import db, User, Exercise
from App.controllers import create_user, get_all_exercises, initialize
import os, csv

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return redirect('/home')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
