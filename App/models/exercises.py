from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    force = db.Column(db.String)
    level = db.Column(db.String)
    mechanic = db.Column(db.String)
    equipment = db.Column(db.String)
    primaryMuscles = db.Column(db.String)
    secondaryMuscles = db.Column(db.String)
    instructions = db.Column(db.String)
    category = db.Column(db.String)
    image1 = db.Column(db.String)
    image2 = db.Column(db.String)

    def __init__(self, id, name, force, level, mechanic, equipment, primaryMuscles, secondaryMuscles, instructions, category, image1, image2):
        self.id
        self.name = name
        self.force = force
        self.level = level
        self.mechanic = mechanic
        self.equipment = equipment
        self.primaryMuscles = primaryMuscles
        self.secondaryMuscles = secondaryMuscles
        self.instructions = instructions
        self.category = category
        self.image1 = image1
        self.image2 = image2

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'force': self.force,
            'level': self.level,
            'mechanic': self.mechanic,
            'equipment': self.equipment,
            'primaryMuscles': self.primaryMuscles,
            'secondaryMuscles': self.secondaryMuscles,
            'instructions': self.instructions,
            'category': self.category,
            'image1': self.image1,
            'image2': self.image2
        }