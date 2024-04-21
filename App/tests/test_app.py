import os, tempfile, pytest, logging, unittest, json
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Exercise, Favorite
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

class TestFavoriteModel:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, empty_db):
        self.client = empty_db
        self.user = User("bobby", "bobpass")
        self.exercise = Exercise(id=999, name="test-exercise", category="strength", force="pull", level="beginner", mechanic="isolation", equipment="machine", primaryMuscles="abdominals", secondaryMuscles="obliques", instructions="Sit down on the ab crunch machine and select a weight you are comfortable with.", image1="Crunches-1.png", image2="Crunches-2.png)")
        db.session.add(self.user)
        db.session.add(self.exercise)
        db.session.commit()

        yield  # This is where the testing happens

        Favorite.query.delete()
        User.query.delete()
        Exercise.query.delete()
        db.session.commit()

    def test_favorite_creation(self):
        favorite = Favorite(self.user, self.exercise)
        db.session.add(favorite)
        db.session.commit()
        assert favorite.user_id == self.user.id
        assert favorite.exercise_id == self.exercise.id

    def test_favorite_serialization(self):
        favorite = Favorite(self.user, self.exercise)
        db.session.add(favorite)
        db.session.commit()
        serialized = favorite.serialize()
        assert serialized['id'] == favorite.id
        assert serialized['user'] == favorite.user
        assert serialized['exercise'] == favorite.exercise
'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        

