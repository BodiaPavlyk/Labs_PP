from app import program
from controllers.announcement_controller import AnnouncementController
from flask import request


@program.route("/A")
def hello1():
    return "Good"


@program.route("/Announcement", methods=['POST'])
def create_announcement():
    announcement_controller = AnnouncementController()
    return announcement_controller.Create(request.args)


@program.route("/Announcement", methods=['GET'])
def users_announcement():
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_by_User(request.args)


@program.route("/Announcement/public", methods=['GET'])
def public_announcement():
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_Public()


@program.route("/Announcement/local", methods=['GET'])
def local_announcement():
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_Local(request.args)


@program.route("/Announcement/", methods=['PUT'])
def update_announcement():
    announcement_controller = AnnouncementController()
    return announcement_controller.Update(request.args)


@program.route("/Announcement/", methods=['DELETE'])
def delete_announcement():
    announcement_controller = AnnouncementController()
    return announcement_controller.Delete(request.args)
