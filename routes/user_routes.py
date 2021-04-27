from app import program, token_required
from controllers.user_controller import UserController
from flask import request, render_template, jsonify
from flask_mail import Message
from models.user import User
from Email import Email, bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
import json
import random, string

program.config['SECRET_KEY'] = 'super-secret'


# http://127.0.0.1:5000/User?user_name=name&first_name=fname&last_name=lm&email=name@gmail.com&password=1111&location=Lviv


@program.route("/login", methods=['POST'])
def login_user():
    user_controller = UserController()
    return user_controller.login(request.get_json())


@program.route("/register", methods=['POST'])
def register_user():
    user_controller = UserController()
    return user_controller.registration(request.get_json())


# http://127.0.0.1:5000/User?user_name=name
@program.route("/User/get", methods=['POST'])
@token_required
def read_user(current_user):
    user_controller = UserController()
    return user_controller.Read(current_user)


# http://127.0.0.1:5000/User?user_name=name&new_user_name=NAME&new_first_name=FNAME&new_last_name=LM&email=name1@gmail.com&new_password=2222&new_location=LVIV
@program.route("/User/edit", methods=['POST'])
@token_required
def update_user(current_user):
    user_controller = UserController()
    return user_controller.Update(request.get_json(), current_user)


# http://127.0.0.1:5000/User?user_name=NAME
@program.route("/User/delete", methods=['POST'])
@token_required
def delete_user(current_user):
    user_controller = UserController()
    return user_controller.Delete(current_user)
