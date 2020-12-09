from flask import jsonify
from database import db
from models.user import User
from werkzeug.security import generate_password_hash


class UserController(object):

    def __init__(self, user=User()):
        self.user = user

    def Create(self, user_parameters=None):
        self.user.user_name = user_parameters.get('user_name')
        self.user.first_name = user_parameters.get('first_name')
        self.user.last_name = user_parameters.get('last_name')
        self.user.email = user_parameters.get('email')
        if user_parameters.get('password'):
            self.user.password = generate_password_hash(user_parameters.get('password'))
        self.user.location = user_parameters.get('location')

        if self.user.Any_Empty_Field():
            return jsonify(message='Bad request. Contain empty field(s)!', status=400)
        if self.user.Invalid_Data():
            return jsonify(message='Bad request. Invalid data!', status=400)
        if User.Get_from_db(user_name=self.user.user_name) or User.Get_from_db(email=self.user.email):
            return jsonify(message='User with such user_name/email already exist!', status=409)

        db.session.add(self.user)
        db.session.commit()
        return jsonify(message='Successfully created user!', status=200)

    def Read(self, user_name=None):

        user_name = user_name.get('user_name')
        self.user = User.Get_from_db(user_name=user_name)
        if self.user:
            return jsonify(message='Successful operation!', status=200)

        return jsonify(message='User not found!', status=404)

    def Update(self, user_parameters=None):

        user_name = user_parameters.get("user_name")
        self.user = User.Get_from_db(user_name=user_name)
        if not self.user:
            return jsonify(message='User not found!', status=404)

        updated_user = User()
        if user_parameters.get('new_user_name'):
            updated_user.user_name = user_parameters.get('new_user_name')
        else:
            updated_user.user_name = self.user.user_name

        if user_parameters.get('new_first_name'):
            updated_user.first_name = user_parameters.get('new_first_name')
        else:
            updated_user.first_name = self.user.first_name

        if user_parameters.get('new_last_name'):
            updated_user.last_name = user_parameters.get('new_last_name')
        else:
            updated_user.last_name = self.user.last_name

        if user_parameters.get('new_email'):
            updated_user.email = user_parameters.get('new_email')
        else:
            updated_user.email = self.user.email

        if user_parameters.get('new_password'):
            updated_user.password = generate_password_hash(user_parameters.get('new_password'))
        else:
            updated_user.password = self.user.password

        if user_parameters.get('new_location'):
            updated_user.location = user_parameters.get('new_location')
        else:
            updated_user.location = self.user.location

        user_by_name = User.Get_from_db(user_name=updated_user.user_name)
        user_by_email = User.Get_from_db(email=updated_user.email)
        if (user_by_name and user_by_name != self.user) or (user_by_email and user_by_email != self.user):
            return jsonify(message='User with such user_name/email already exist!', status=409)

        if updated_user.Invalid_Data():
            return jsonify(message='Bad request. Invalid data!', status=400)

        #self.user=updated_user
        #db.session.merge(self.user)
        #db.session.flush()
        User.query.filter_by(id=self.user.id).update({
            'user_name':updated_user.user_name,
            'first_name':updated_user.first_name,
            'last_name':updated_user.last_name,
            'email':updated_user.email,
            'password':updated_user.password,
            'location':updated_user.location})
        #db.session.add(self.user)
        db.session.commit()
        return jsonify(message='Successful update operation!', status=200)

    def Delete(self, user_name=None):

        user_name = user_name.get('user_name')
        self.user = User.Get_from_db(user_name=user_name)
        if self.user:
            db.session.delete(self.user)
            db.session.commit()
            return jsonify(message='Successful delete operation!', status=200)

        return jsonify(message='User not found!', status=404)
