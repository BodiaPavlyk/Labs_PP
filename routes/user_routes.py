from app import program
from controllers.user_controller import UserController
from flask import request


@program.route("/U")
def hello2():
    return "Good"


@program.route("/User", methods=['POST'])
def create_user():
    user_controller = UserController()
    return user_controller.Create(request.args)


@program.route("/User/", methods=['GET'])
def read_user():
    user_controller = UserController()
    return user_controller.Read(request.args)


@program.route("/User/", methods=['PUT'])
def update_user():
    user_controller = UserController()
    return user_controller.Update(request.args)

@program.route("/User/", methods=['DELETE'])
def delete_user():
    user_controller = UserController()
    return user_controller.Delete(request.args)
