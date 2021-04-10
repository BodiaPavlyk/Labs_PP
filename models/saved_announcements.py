from re import *
from database import db


class Saved(db.Model):

    __tablename__ = 'saved'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    announcement_id = db.Column(db.Integer, db.ForeignKey('announcement.id'))

    def __init__(self,
                 user_id=None,
                 announcement_id=None):
        self.user_id = user_id
        self.announcement_id = announcement_id

    def Any_Empty_Field(self):
        if not self.user_id:
            return True
        if not self.announcement_id:
            return True
        return False


    @classmethod
    def Get_from_db(self, user_id=None):
        if user_id:
            return Saved.query.filter_by(user_id=user_id).all()
        return None