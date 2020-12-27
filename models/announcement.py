from database import db
from datetime import datetime


class Announcement(db.Model):
    
    __tablename__ = 'announcement'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    theme = db.Column(db.String(50), nullable=False)
    type_of_announcement = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    date_of_publication = db.Column(db.DATETIME, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User', backref='announcement')

    def __init__(self,
                 name=None,
                 theme=None,
                 type_of_announcement=None,
                 description=None,
                 location=None,
                 creator=None):
        self.name = name
        self.theme = theme
        self.type_of_announcement = type_of_announcement
        self.description = description
        self.location = location
        self.creator = creator

    def Any_Empty_Field(self):
        if not self.name:
            return True
        if not self.theme:
            return True
        if not self.type_of_announcement:
            return True
        if not self.description:
            return True
        if self.type_of_announcement == "local" and not self.location:
            return True
        if not self.creator:
            return True
        return False

    @classmethod
    def Get_from_db(self, user_id=None, announcement_id=None, type_of_announcement=None, location=None):
        if announcement_id:
            return Announcement.query.filter_by(id=announcement_id).first()
        if user_id:
            return Announcement.query.filter_by(user_id=user_id).all()
        if type_of_announcement:
            return Announcement.query.filter_by(type_of_announcement=type_of_announcement).all()
        if location:
            return Announcement.query.filter_by(location=location).all()