from flask import jsonify, make_response
from database import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
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
            password = generate_password_hash(user_parameters.get('password'))
        location = user_parameters.get('location')
        user = User(user_name, first_name, last_name, email, password, location)
        if user.Any_Empty_Field():
            return jsonify(message='Bad request. Contain empty field(s)!', status=400)
        if user.Invalid_Data():
            return jsonify(message='Bad request. Invalid data!', status=400)
        if User.Get_from_db(user_name=user_name) or User.Get_from_db(email=email):
            return jsonify(message='User with such user_name/email already exist!', status=409)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="Registered successfully! Now, please login", status=200)

    def login(self, user_parameters=None):
        if not user_parameters:
            return make_response('Could verify!', 401, {'WWW-authenticate': 'Basic realm="Login Required'})
        user_name = user_parameters.username
        password = user_parameters.password
        if not user_name or not password:
            return jsonify(message="Missing values!", status=400)
        user = User.Get_from_db(user_name=user_name)
        if not user:
            return make_response('Couldn`t verify!', 401, {'WWW-authenticate': 'Basic realm="Login Required'})
        elif check_password_hash(user.password, password):
            access_token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, program.config["SECRET_KEY"])
            return jsonify(message="User was logged in", token=access_token.decode('UTF-8'), status=200)
        return make_response('Couldn`t verify!', 401, {'WWW-authenticate': 'Basic realm="Login Required'})

    def Read(self, current_user=None):
        if current_user:
            return jsonify(info=[current_user.user_name, current_user.first_name, current_user.last_name, current_user.email, current_user.location], status=200)

        return jsonify(message='User not found!', status=404)

    def Update(self, user_parameters=None, current_user=None):

        if not current_user:
            return jsonify(message='User not found!', status=404)

        updated_user = User()
        if user_parameters.get('new_user_name'):
            updated_user.user_name = user_parameters.get('new_user_name')
        else:
            updated_user.user_name = current_user.user_name

        if user_parameters.get('new_first_name'):
            updated_user.first_name = user_parameters.get('new_first_name')
        else:
            updated_user.first_name = current_user.first_name

        if user_parameters.get('new_last_name'):
            updated_user.last_name = user_parameters.get('new_last_name')
        else:
            updated_user.last_name = current_user.last_name

        if user_parameters.get('new_email'):
            updated_user.email = user_parameters.get('new_email')
        else:
            updated_user.email = current_user.email

        if user_parameters.get('new_password'):
            updated_user.password = generate_password_hash(user_parameters.get('new_password'))
        else:
            updated_user.password = current_user.password

        if user_parameters.get('new_location'):
            updated_user.location = user_parameters.get('new_location')
        else:
            updated_user.location = current_user.location

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
            'password': updated_user.password,
            'location': updated_user.location
        })
        db.session.commit()
        return jsonify(message='Successful update operation!', status=200)

    def Delete(self, user_name=None):

        user_name = user_name.get('user_name')
        user = User.Get_from_db(user_name=user_name)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(message='Successful delete operation!', status=200)

        return jsonify(message='User not found!', status=404)
