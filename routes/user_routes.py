from app import program, token_required
from controllers.user_controller import UserController
from flask import request

program.config['SECRET_KEY'] = 'super-secret'

#http://127.0.0.1:5000/User?user_name=name&first_name=fname&last_name=lm&email=name@gmail.com&password=1111&location=Lviv


@program.route("/login", methods=['POST'])
def login_user():
    user_controller = UserController()
    return user_controller.login(request.authorization)


@program.route("/register", methods=['POST'])
def register_user():
    user_controller = UserController()
    return user_controller.registration(request.args)


#http://127.0.0.1:5000/User?user_name=name
@program.route("/User/", methods=['GET'])
@token_required
def read_user(current_user):
    user_controller = UserController()
    return user_controller.Read(current_user)


#http://127.0.0.1:5000/User?user_name=name&new_user_name=NAME&new_first_name=FNAME&new_last_name=LM&email=name1@gmail.com&new_password=2222&new_location=LVIV
@program.route("/User/", methods=['PUT'])
@token_required
def update_user(current_user):
    user_controller = UserController()
    return user_controller.Update(request.args, current_user)


#http://127.0.0.1:5000/User?user_name=NAME
@program.route("/User/", methods=['DELETE'])
@token_required
def delete_user(current_user):
    user_controller = UserController()
    return user_controller.Delete(current_user)
