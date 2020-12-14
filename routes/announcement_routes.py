from app import program, token_required
from controllers.announcement_controller import AnnouncementController
from flask import request

program.config['SECRET_KEY'] = 'super-secret'

#http://127.0.0.1:5000/Announcement/create?name=Hi!!!&theme=Local&type_of_announcement=local&description=Hello to everyone who logged in! Have a nice day)&location=Stepana Bandery street&user_id=2
@program.route("/Announcement/create", methods=['POST'])
@token_required
def create_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Create(request.args, current_user)


@program.route("/Announcement", methods=['GET'])
@token_required
def users_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_by_User(current_user)


@program.route("/Announcement/public", methods=['GET'])
def public_announcement():
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_Public()


@program.route("/Announcement/local", methods=['GET'])
@token_required
def local_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Read_Local(request.args)


@program.route("/Announcement/edit", methods=['PUT'])
@token_required
def update_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Update(request.args, current_user)


@program.route("/Announcement/", methods=['DELETE'])
@token_required
def delete_announcement(current_user):
    announcement_controller = AnnouncementController()
    return announcement_controller.Delete(request.args, current_user)
