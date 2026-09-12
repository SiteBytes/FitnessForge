import os
import csv
from .user import create_user
from App.database import db
from App.models import Exercise, User


def initialize():
    db.drop_all()
    db.create_all()
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'finalexercises.csv')
    if not os.path.exists(csv_path):
        csv_path = './App/static/finalexercises.csv'
    with open(csv_path, newline='', encoding='utf8') as csvfile:
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


def ensure_db_initialized():
    db.create_all()
    if not User.query.filter_by(username='bob').first():
        initialize()

