from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False, unique=True)
    difficulty = db.Column(db.Integer, nullable=True) #? difficulty rating of exercise, from 1(easy) to 5(hardest)


    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty

    def get_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'difficulty': difficulty
        }