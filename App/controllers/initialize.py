from .user import create_user
from App.database import db
from App.models import Exercise
import csv


def initialize():
    db.drop_all()
    db.create_all()
    with open('finalexercises.csv', newline='', encoding='utf8') as csvfile:
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
