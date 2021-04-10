from models.announcement import Announcement
from flask import jsonify
from database import db
from models.user import User
from models.saved_announcements import Saved


class AnnouncementController(object):
    def Create(self, announcement_parameters=None, current_user=None):
        name = announcement_parameters.get('name')
        theme = announcement_parameters.get('theme')
        type_of_announcement = announcement_parameters.get('type_of_announcement')
        description = announcement_parameters.get('description')
        if type_of_announcement == "local":
            location = announcement_parameters.get('location')
        else:
            location = ""
        creator = User.query.filter_by(id=current_user.id).first()
        announcement = Announcement(name, theme, type_of_announcement, description, location, creator)
        if announcement.Any_Empty_Field():
            return jsonify(message='Bad request. Contain empty field(s)!', status=400)

        db.session.add(announcement)
        db.session.commit()
        return jsonify(message='Successfully created announcement!', status=200)

    def Read_by_User(self, user_id=None):
        list_of_announcements = Announcement.Get_from_db(user_id=user_id.id)
        if list_of_announcements:
            return jsonify(list_of_announcements=[[i.id, i.name, i.theme, i.description, (User.query.filter_by(id=i.user_id).first()).email, i.date_of_publication] for i in list_of_announcements], status=200)

        return jsonify(message='Announcements not found!', status=404)

    def Read_Public(self):
        list_of_announcements = Announcement.Get_from_db(type_of_announcement="public")
        if list_of_announcements:
            return jsonify(list_of_public_announcements=[[i.id, i.name, i.theme, i.description, (User.query.filter_by(id=i.user_id).first()).email, i.date_of_publication] for i in list_of_announcements], status=200)

        return jsonify(message='Announcements not found!', status=404)

    def Read_Local(self, location=None):

        location = location.get('location')
        list_of_announcements = Announcement.Get_from_db(location=location)
        if list_of_announcements:
            return jsonify(list_of_local_announcements=[[i.id, i.name, i.theme, i.description, i.location, (User.query.filter_by(id=i.user_id).first()).email, i.date_of_publication] for i in list_of_announcements], status=200)

        return jsonify(message='Announcements not found!', status=404)

    def get_all_saved(self, current_user=None):
        list_of_saved_announcements = Saved.Get_from_db(user_id=current_user.id)
        list_of_announcements = []
        if not list_of_saved_announcements:
            return jsonify(message='There is no saved announcements', status=200)
        for i in list_of_saved_announcements:
            an = Announcement.Get_from_db(announcement_id=i.announcement_id)
            list_of_announcements.append([an.id, an.name, an.theme, an.description, an.location, (User.query.filter_by(id=an.user_id).first()).email], an.date_of_publication)
        return jsonify(list_of_local_announcements=list_of_announcements, status=200)


    def add_to_saved(self, announcement_id=None, current_user=None):

        user = User.query.filter_by(id=current_user.id).first()
        announcement = Announcement.Get_from_db(announcement_id=announcement_id)
        list_of_saved_announcements = Saved.Get_from_db(user_id=current_user.id)
        for i in list_of_saved_announcements:
            if str(i.announcement_id) == announcement_id:
                return jsonify(message='You have already saved this message', status=400)
        if not announcement:
            return jsonify(message='Announcements not found!', status=404)
        saved_announcement = Saved(user.id, announcement.id)
        db.session.add(saved_announcement)
        db.session.commit()
        return jsonify(message='The message is saved!', status=200)


    def delete_from_saved(self, announcement_id=None, current_user=None):
        user = User.query.filter_by(id=current_user.id).first()
        announcement = Announcement.Get_from_db(announcement_id=announcement_id)
        saved_announcement = Saved.query.filter_by(user_id=user.id, announcement_id=announcement.id).first()
        if not saved_announcement:
            return jsonify(message='The announcement is already deleted from saved!', status=404)
        else:
            db.session.delete(saved_announcement)
            db.session.commit()
            return jsonify(message='Successful delete operation!', status=200)


    def Update(self, announcement_parameters=None, current_user=None):

        announcement_id = announcement_parameters.get('announcement_id')
        announcement = Announcement.Get_from_db(announcement_id=announcement_id)

        if not announcement:
            return jsonify(message='Announcements not found!', status=404)
        elif announcement.user_id != current_user.id:
            return jsonify(message='You don`t have rights to do this!', status=403)
        updated_announcement = Announcement()
        if announcement_parameters.get('new_name'):
            updated_announcement.name = announcement_parameters.get('new_name')
        else:
            updated_announcement.name = announcement.name

        if announcement_parameters.get('new_theme'):
            updated_announcement.theme = announcement_parameters.get('new_theme')
        else:
            updated_announcement.theme = announcement.theme

        if announcement_parameters.get('new_type_of_announcement'):
            updated_announcement.type_of_announcement = announcement_parameters.get('new_type_of_announcement')
        else:
            updated_announcement.type_of_announcement = announcement.type_of_announcement

        if announcement_parameters.get('new_description'):
            updated_announcement.description = announcement_parameters.get('new_description')
        else:
            updated_announcement.description = announcement.description

        if announcement_parameters.get('new_location'):
            updated_announcement.location = announcement_parameters.get('new_location')
        else:
            updated_announcement.location = announcement.location

        Announcement.query.filter_by(id=announcement.id).update({
            'name': updated_announcement.name,
            'theme': updated_announcement.theme,
            'type_of_announcement': updated_announcement.type_of_announcement,
            'description': updated_announcement.description,
            'location': updated_announcement.location
        })

        db.session.commit()
        return jsonify(message='Successful update operation!', status=200)

    def Delete(self, announcement_id=None, current_user=None):
        announcement_id = announcement_id.get('announcement_id')
        announcement = Announcement.Get_from_db(announcement_id=announcement_id)
        if not announcement:
            return jsonify(message='Announcements not found!', status=404)
        elif announcement.user_id != current_user.id:
            return jsonify(message='You don`t have rights to do this!', status=403)
        if announcement:
            db.session.delete(announcement)
            db.session.commit()
            return jsonify(message='Successful delete operation!', status=200)

    def filter(self, parameter=None):
        list_of_announcements = Announcement.query.filter(Announcement.name == parameter or Announcement.location == parameter).all()
        return jsonify(list=[[i.id, i.name, i.theme, i.description, i.location, (User.query.filter_by(id=i.user_id).first()).email, i.date_of_publication] for i in list_of_announcements], status=200)