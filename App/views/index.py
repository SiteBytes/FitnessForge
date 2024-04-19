from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db, User, Exercise
from App.controllers import create_user, get_all_exercises
import os, csv

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    with open('splitexercises.csv', newline='', encoding='utf8') as csvfile:
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
    create_user('bob', 'bobpass')
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})


@index_views.route('/exercises', methods=['GET'])
def list_exercises():
    exercises = get_all_exercises()
    return render_template('exercises.html', exercises=exercises)