from App.database import db

class Favorite(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
        exercise = db.relationship('Exercise', backref='favorites')
        user = db.relationship('User', backref='favorites')

        def __init__(self, user, exercise):
            self.user_id = user.id
            self.exercise_id = exercise.id

        def get_json(self):
            return {
                'id': self.id,
                'user': self.user,
                'exercise': self.exercise
            }