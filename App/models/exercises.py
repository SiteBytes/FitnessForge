from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Exercise(db.Model):
    __tablename__ = 'exercise'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    force = db.Column(db.String, nullable=True)
    level = db.Column(db.String, nullable=True)
    mechanic = db.Column(db.String, nullable=True)
    equipment = db.Column(db.String, nullable=True)
    primaryMuscles = db.Column(db.String, nullable=True)
    secondaryMuscles = db.Column(db.String, nullable=True)
    instructions = db.Column(db.String, nullable=True)
    category = db.Column(db.String, nullable=True)
    images = db.Column(db.String, nullable=True)

    def __init__(self, name, force, level, mechanic, equipment, primaryMuscles, secondaryMuscles, instructions, category, images, id):
        self.name = name
        self.force = force
        self.level = level
        self.mechanic = mechanic
        self.equipment = equipment
        self.primaryMuscles = primaryMuscles
        self.secondaryMuscles = secondaryMuscles
        self.instructions = instructions
        self.category = category
        self.images = images
        self.id = id

    def get_json(self):
        return{
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
            'images': self.images
        }