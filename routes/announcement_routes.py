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


@program.route("/Announcement/getInfo", methods=['POST'])
@token_required
def getinfo_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_certain(request.get_json().get("id"))


@program.route("/Announcement", methods=['POST'])
@token_required
def users_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_by_User(current_user)


@program.route("/Announcement/public", methods=['POST'])
def public_announcement():
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_Public()


@program.route("/Announcement/local", methods=['POST'])
@token_required
def local_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_Local()


@program.route("/Announcement/edit", methods=['POST'])
@token_required
def update_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Update(request.get_json(), current_user)


@program.route("/Announcement/delete", methods=['POST'])
@token_required
def delete_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Delete(request.get_json(), current_user)


@program.route("/saved_announcement/add", methods=['POST'])
@token_required
def add_saved_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.add_to_saved(request.get_json().get("id"), current_user)


@program.route("/saved_announcement/delete", methods=['POST'])
@token_required
def delete_saved_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.delete_from_saved(request.get_json().get("id"), current_user)


@program.route("/saved_announcement", methods=['POST'])
@token_required
def users_saved_announcements(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.get_all_saved(current_user)


@program.route("/filter", methods=['POST'])
@token_required
def filter(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.filter(request.get_json().get("parameter"))