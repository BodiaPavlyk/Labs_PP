from app import program, token_required
from controllers.announcement_controller import AnnouncementController
from flask import request
import json

program.config['SECRET_KEY'] = 'super-secret'

#http://127.0.0.1:5000/Announcement/create?name=Hi!!!&theme=Local&type_of_announcement=local&description=Hello to everyone who logged in! Have a nice day)&location=Stepana Bandery street&user_id=2
@program.route("/Announcement/create", methods=['POST'])
@token_required
def create_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Create(request.get_json(), current_user)


@program.route("/Announcement", methods=['GET'])
@token_required
def users_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_by_User(request.get_json())


@program.route("/Announcement/public", methods=['GET'])
def public_announcement():
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_Public()


@program.route("/Announcement/local", methods=['GET'])
@token_required
def local_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_Local(request.get_json())


@program.route("/Announcement/edit", methods=['PUT'])
@token_required
def update_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Update(request.get_json(), current_user)


@program.route("/Announcement/delete", methods=['DELETE'])
@token_required
def delete_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Delete(request.get_json(), current_user)


@program.route("/saved_announcement/add", methods=['POST'])
@token_required
def add_saved_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.add_to_saved(request.get_json().get("id"), current_user)


@program.route("/saved_announcement/delete", methods=['DELETE'])
@token_required
def delete_saved_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.delete_from_saved(request.get_json().get("id"), current_user)


@program.route("/saved_announcement", methods=['GET'])
@token_required
def users_saved_announcements(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.get_all_saved(current_user)


@program.route("/filter", methods=['GET'])
@token_required
def filter(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.filter(request.get_json().get("parameter"))