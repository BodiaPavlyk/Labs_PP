from flask import jsonify, make_response
from models.announcement import Announcement
from database import db
from models.user import User
from Email import bcrypt
from app import program
import jwt, json
import datetime


class UserController(object):

    def registration(self, user_parameters=None):
        user_name = user_parameters.get('user_name')
        first_name = user_parameters.get('first_name')
        last_name = user_parameters.get('last_name')
        email = user_parameters.get('email')
        if user_parameters.get('password'):
            password = bcrypt.generate_password_hash(user_parameters.get('password'))
        user = User(user_name, first_name, last_name, email, password)
        if user.Any_Empty_Field():
            return jsonify(message='Bad request. Contain empty field(s)!', status=400)
        if user.Invalid_Data():
            return jsonify(message='Bad request. Invalid data!', status=400)
        if not bcrypt.check_password_hash(password, user_parameters.get('confirm_password')):
            return jsonify(message='Passwords don`t match!', status=400)
        if User.Get_from_db(user_name=user_name) or User.Get_from_db(email=email):
            return jsonify(message='User with such user_name/email already exist!', status=409)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="Registered successfully!", status=200)

    def login(self, user_parameters=None):
        if not user_parameters:
            return jsonify(message='Couldn`t verify!', status=401)
        email = user_parameters['email']
        password = user_parameters['password']
        if not email or not password:
            return jsonify(message="Missing values!", status=400)
        user = User.Get_from_db(email=email)
        if not user:
            return jsonify(message='Couldn`t verify!', status=401)
        elif bcrypt.check_password_hash(user.password, password):
            access_token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90)}, program.config["SECRET_KEY"])
            return jsonify(message="User was logged in", token=access_token, status=200)
        return jsonify(message='Couldn`t verify!', status=401)

    def Read(self, current_user=None):
        if current_user:
            count = len(Announcement.query.filter_by(user_id=current_user.id).all())
            return jsonify(info=[current_user.user_name, current_user.first_name, current_user.last_name, current_user.email, count], status=200)

        return jsonify(message='User not found!', status=404)


    def Update(self, user_parameters=None, current_user=None):

        user = User.Get_from_db(user_name=current_user.user_name)

        if not current_user:
            return jsonify(message='User not found!', status=404)

        updated_user = User()
        if user_parameters.get('user_name'):
            updated_user.user_name = user_parameters.get('user_name')
        else:
            updated_user.user_name = current_user.user_name

        if user_parameters.get('first_name'):
            updated_user.first_name = user_parameters.get('first_name')
        else:
            updated_user.first_name = current_user.first_name

        if user_parameters.get('last_name'):
            updated_user.last_name = user_parameters.get('last_name')
        else:
            updated_user.last_name = current_user.last_name

        if user_parameters.get('email'):
            updated_user.email = user_parameters.get('email')
        else:
            updated_user.email = current_user.email

        if user_parameters.get('password'):
            updated_user.password = bcrypt.generate_password_hash(user_parameters.get('password'))
        else:
            updated_user.password = current_user.password

        user_by_name = User.Get_from_db(user_name=updated_user.user_name)
        user_by_email = User.Get_from_db(email=updated_user.email)
        if (user_by_name and user_by_name != user) or (user_by_email and user_by_email != user):
            return jsonify(message='User with such user_name/email already exist!', status=409)

        if updated_user.Invalid_Data():
            return jsonify(message='Bad request. Invalid data!', status=400)

        User.query.filter_by(id=user.id).update({
            'user_name': updated_user.user_name,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'password': updated_user.password
        })
        db.session.commit()
        return jsonify(message='Successful update operation!', status=200)

    def Delete(self, user_name=None):

        user = User.Get_from_db(user_name=user_name.user_name)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(message='Successful delete operation!', status=200)

        return jsonify(message='User not found!', status=404)
