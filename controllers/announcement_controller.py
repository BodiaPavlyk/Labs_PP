from models.announcement import Announcement
from flask import jsonify
from database import db
from models.user import User


class AnnouncementController(object):

    def __init__(self, announcement=Announcement()):
        self.announcement = announcement

    def Create(self, announcement_parameters=None):
        self.announcement.name = announcement_parameters.get('name')
        self.announcement.theme = announcement_parameters.get('theme')
        self.announcement.type_of_announcement = announcement_parameters.get('type_of_announcement')
        self.announcement.description = announcement_parameters.get('description')
        self.announcement.location = announcement_parameters.get('location')
        self.announcement.creator = User.query.filter_by(id=announcement_parameters.get('user_id')).first()

        if self.announcement.Any_Empty_Field():
            return jsonify(message='Bad request. Contain empty field(s)!', status=400)

        db.session.add(self.announcement)
        db.session.commit()
        return jsonify(message='Successfully created announcement!', status=200)

    def Read_by_User(self, user_id=None):

        user_id = user_id.get('user_id')
        list_of_announcements = Announcement.Get_from_db(user_id=user_id)
        if list_of_announcements:
            return jsonify(message='Successful operation!', status=200)

        return jsonify(message='Announcements not found!', status=404)

    def Read_Public(self):
        list_of_announcements = Announcement.Get_from_db(type_of_announcement="public")
        if list_of_announcements:
            return jsonify(message='Successful operation!', status=200)

        return jsonify(message='Announcements not found!', status=404)

    def Read_Local(self, location=None):

        location = location.get('location')
        list_of_announcements = Announcement.Get_from_db(location=location)
        if list_of_announcements:
            return jsonify(message='Successful operation!', status=200)

        return jsonify(message='Announcements not found!', status=404)

    def Update(self, announcement_parameters=None):
        announcement_id = announcement_parameters.get('announcement_id')
        self.announcement = Announcement.Get_from_db(announcement_id=announcement_id)
        if not self.announcement:
            return jsonify(message='Announcements not found!', status=404)

        updated_announcement = Announcement()
        if announcement_parameters.get('new_name'):
            updated_announcement.name = announcement_parameters.get('new_name')
        else:
            updated_announcement.name = self.announcement.name

        if announcement_parameters.get('new_theme'):
            updated_announcement.theme = announcement_parameters.get('new_theme')
        else:
            updated_announcement.theme = self.announcement.theme

        if announcement_parameters.get('new_type_of_announcement'):
            updated_announcement.type_of_announcement = announcement_parameters.get('new_type_of_announcement')
        else:
            updated_announcement.type_of_announcement = self.announcement.type_of_announcement

        if announcement_parameters.get('new_description'):
            updated_announcement.description = announcement_parameters.get('new_description')
        else:
            updated_announcement.description = self.announcement.description

        if announcement_parameters.get('new_location'):
            updated_announcement.location = announcement_parameters.get('new_location')
        else:
            updated_announcement.location = self.announcement.location

        Announcement.query.filter_by(id=self.announcement.id).update({
            'name': updated_announcement.name,
            'theme': updated_announcement.theme,
            'type_of_announcement': updated_announcement.type_of_announcement,
            'description': updated_announcement.description,
            'location': updated_announcement.location
        })

        db.session.commit()
        return jsonify(message='Successful update operation!', status=200)

    def Delete(self, announcement_id=None):
        announcement_id = announcement_id.get('announcement_id')
        self.announcement = Announcement.Get_from_db(announcement_id=announcement_id)
        if self.announcement:
            db.session.delete(self.announcement)
            db.session.commit()
            return jsonify(message='Successful delete operation!', status=200)

        return jsonify(message='Announcements not found!', status=404)
