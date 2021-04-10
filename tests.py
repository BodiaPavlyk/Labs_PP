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

    def test1_registration(self):
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

    def test1_1_registration(self):
        data = {
            "user_name": "bohdan",
            "first_name": "testf",
            "last_name": "testl",
            "email": "test@gmail.com",
            "password": "1111",
            "location": "Lviv"
        }
        response = self._program.open('/register', method='POST', json=data)
        self.assertEqual(200, response.status_code)

    def test1_2_registration(self):
        data = {
            "first_name": "testf",
            "last_name": "testl",
            "email": "test@gmail.com",
            "password": "1111",
            "location": "Lviv"
        }
        response = self._program.open('/register', method='POST', json=data)
        self.assertEqual(200, response.status_code)

    def test2_successful_signup(self):
        payload = {
            "user_name": "testname",
            "password": "1111"
        }
        response = self._program.open('/login', method='POST', json=payload)
        self.assertEqual(response.status_code, 200)

    def test2_unsuccessful_signup(self):
        payload = {
            "password": "1111"
        }
        response = self._program.open('/login', method='POST')
        self.assertEqual(response.status_code, 401)

    def test2_2_unsuccessful_signup(self):
        payload = {
            "user_name": "VIKA",
            "password": "1111"
        }
        response = self._program.open('/login', method='POST', json=payload)
        self.assertEqual(response.status_code, 401)

    def test3_read_user(self):
        with program.app_context():
            user = User.query.filter_by(user_name='testname').first()
            access_token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                      program.config["SECRET_KEY"])
            headers = {'x-access-token': access_token}
            responce = self._program.open('/User/', method='GET', headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)

    def test4_update_user(self):
        with program.app_context():
            user = User.query.filter_by(user_name='testname').first()
            access_token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                      program.config["SECRET_KEY"])
            dataf = { "user_name":"testname",
                    "new_user_name":"NAME",
                    "new_first_name":"FNAME",
                    "new_last_name":"LM",
                    "email":"test@gmail.com",
                    "new_password":"2222",
                    "new_location":"LVIV"
                    }
            headers = {'x-access-token': access_token}
            responce = self._program.put('/User/', json=dataf, headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)

    def test5_create_an(self):
        with program.app_context():
            user = User.query.filter_by(user_name='NAME').first()
            access_token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                      program.config["SECRET_KEY"])
            data={
                'name':'testing!!!',
                'theme':'Welcome',
                'type_of_announcement':'public',
                'description':"enjoy testing!!!",
                'location':'somewhere'}
            headers = {'x-access-token': access_token}
            responce = self._program.post('/Announcement/create', json=data, headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)

    def test5_5_create_an(self):
        with program.app_context():
            user = User.query.filter_by(user_name='NAME').first()
            access_token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                      program.config["SECRET_KEY"])
            data={
                'theme':'Welcome',
                'type_of_announcement':'public',
                'description':"enjoy testing!!!",
                'location':'somewhere'}
            headers = {'x-access-token': access_token}
            responce = self._program.post('/Announcement/create', json=data, headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)

    def test6_read_an(self):
        with program.app_context():
            user = User.query.filter_by(user_name='NAME').first()
            access_token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                      program.config["SECRET_KEY"])
            headers = {'x-access-token': access_token}
            responce = self._program.get('/Announcement', headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)

    def test7_local_an(self):
        with program.app_context():
            user = User.query.filter_by(user_name='NAME').first()
            access_token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                      program.config["SECRET_KEY"])
            headers = {'x-access-token': access_token}
            responce = self._program.get('/Announcement/local', headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)

    def test8_update_an(self):
        with program.app_context():
            user = User.query.filter_by(user_name='NAME').first()
            access_token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                      program.config["SECRET_KEY"])
            ann = Announcement.query.filter_by(name="testing!!!").first()
            data = { "announcement_id": ann.id,
                    "new_name":"NAME",
                    "new_theme":"THEME",
                    "new_type_of_announcement":"PUBLIC",
                    "new_description":"DESCR",
                    "new_location":"LOCATION"
                    }
            headers = {'x-access-token': access_token}
            responce = self._program.put('/Announcement/edit', json=data, headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)

    def test8_8_update_an(self):
        with program.app_context():
            user = User.query.filter_by(user_name='NAME').first()
            access_token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                      program.config["SECRET_KEY"])
            ann = Announcement.query.filter_by(name="Hello world").first()
            data = { "announcement_id": ann.id,
                    "new_name":"NAME",
                    "new_theme": "THEME",
                    "new_type_of_announcement":"PUBLIC",
                    "new_description":"DESCR",
                    "new_location":"LOCATION"
                    }
            headers = {'x-access-token': access_token}
            responce = self._program.put('/Announcement/edit', json=data, headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)

    def test8_8_8_update_an(self):
        with program.app_context():
            user = User.query.filter_by(user_name='NAME').first()
            access_token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                      program.config["SECRET_KEY"])
            ann = Announcement.query.filter_by(name="Hello world").first()
            data = { "announcement_id": 100,
                    "new_name":"NAME",
                    "new_theme": "THEME",
                    "new_type_of_announcement":"PUBLIC",
                    "new_description":"DESCR",
                    "new_location":"LOCATION"
                    }
            headers = {'x-access-token': access_token}
            responce = self._program.put('/Announcement/edit', json=data, headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)

    def test9_delete_an(self):
        with program.app_context():
            user = User.query.filter_by(user_name='NAME').first()
            access_token = jwt.encode(
                {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                program.config["SECRET_KEY"])
            ann = Announcement.query.filter_by(name="NAME").first()
            data={"announcement_id": ann.id}
            headers = {'x-access-token': access_token}
            responce = self._program.delete('/Announcement/', json=data, headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)

    def test9_9_delete_an(self):
        with program.app_context():
            user = User.query.filter_by(user_name='NAME').first()
            access_token = jwt.encode(
                {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                program.config["SECRET_KEY"])
            ann = Announcement.query.filter_by(name="Hello world").first()
            data={"announcement_id": ann.id}
            headers = {'x-access-token': access_token}
            responce = self._program.delete('/Announcement/', json=data, headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)

    def test9_9_9_delete_an(self):
        with program.app_context():
            user = User.query.filter_by(user_name='NAME').first()
            access_token = jwt.encode(
                {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                program.config["SECRET_KEY"])
            ann = Announcement.query.filter_by(name="NAME").first()
            data={"announcement_id": 100}
            headers = {'x-access-token': access_token}
            responce = self._program.delete('/Announcement/', json=data, headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)

    def test_delete_user(self):
        with program.app_context():
            user = User.query.filter_by(user_name="NAME").first()
            access_token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                      program.config["SECRET_KEY"])

            headers = {'x-access-token': access_token}
            responce = self._program.delete('/User/', headers=headers)
            statuscode = responce.status_code
            self.assertEqual(statuscode, 200)


if __name__ == '__main__':
    unittest.main()
