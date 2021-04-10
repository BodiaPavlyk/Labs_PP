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


@program.route('/ResetPassword', methods=["POST", "GET"])
def ResetPassword():
    mail = request.get_json().get('email')
    check = User.query.filter_by(email=mail).first()

    if check:
        with program.app_context():
            hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
            check.hash_code = hashCode
            db.session.commit()
            msg = Message('Confirm Password Change', sender=program.config.get('MAIL_USERNAME'), recipients=[mail])
            msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n http://localhost:5000/" + check.hash_code
            Email.send(msg)
            return jsonify(message="OK!", status=200)
    else:
        return jsonify(message="The user with such email was not found!", status=404)


@program.route("/<string:hashCode>", methods=["GET", "POST"])
def hashcode(hashCode):
    check = User.query.filter_by(hash_code=hashCode).first()
    if check:
        if request.method == 'POST':
            request_data = request.get_json()
            password = request_data.get['password']
            check_password = request_data.get['check_password']
            if password == check_password:
                check.password = bcrypt.generate_password_hash(password)
                check.hash_code = None
                db.session.add(check)
                db.session.commit()
                return jsonify(message="OK!", status=200)
            else:
                return jsonify(message="Passwords are different!", status=400)
    else:
        return jsonify(message="Hashcode was not found!", status=404)


# http://127.0.0.1:5000/User?user_name=name
@program.route("/User/get", methods=['GET'])
@token_required
def read_user(current_user):
    user_controller = UserController()
    return user_controller.Read(current_user)


# http://127.0.0.1:5000/User?user_name=name&new_user_name=NAME&new_first_name=FNAME&new_last_name=LM&email=name1@gmail.com&new_password=2222&new_location=LVIV
@program.route("/User/edit", methods=['PUT'])
@token_required
def update_user(current_user):
    user_controller = UserController()
    return user_controller.Update(request.get_json(), current_user)


# http://127.0.0.1:5000/User?user_name=NAME
@program.route("/User/delete", methods=['DELETE'])
@token_required
def delete_user(current_user):
    user_controller = UserController()
    return user_controller.Delete(current_user)
