import unittest
import json
import jwt, datetime
from flask import request
from flask.testing import FlaskClient
from flask_testing import TestCase
from database import db
from app import program
from routes import user_routes
from models.user import User
from controllers.user_controller import UserController
from models.announcement import Announcement
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


class FlaskTest(unittest.TestCase):
    def setUp(self):
        program.config['TESTING'] = True
        program.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        self._program = program.test_client()

    def tearDown(self):
        pass

    def test_registration(self):
        data = {
            "user_name": "testname",
            "first_name": "testf",
            "last_name": "testl",
            "email": "test@gmail.com",
            "password": "1111",
            "location": "Lviv"
        }
        response = self._program.open('/register', method='POST', json=data)
        self.assertEqual(200, response.status_code)

    def test_successful_signup(self):
        payload = json.dumps({
            "user_name": "name",
            "password": "1111"
        })
        # no access
        response = self._program.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(response.status_code, 401)

    def test_read_user(self):
        data = {'user_name': "name"}
        #headers = {'x-access-token': token}
        responce = self._program.get('/User/', json=data)
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)


if __name__ == '__main__':
    unittest.main()
''''
person1 = User(
            user_name='name',
            first_name='fname',
            last_name='lm',
            email='name@gmail.com',
            password='1111',
            location='Lviv'
        )
        ann1 = Announcement(
            name='Hello world',
            theme='Welcome',
            type_of_announcement='public',
            description="Hello everyone! Hope you'll enjoy!!!",
            location=''
            #date_of_publication='2020-12-13 14:23:31.459073',
            #user_id='3'
        )'''