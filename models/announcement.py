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
    creator = db.relationship('User', backref='user')

    def __init__(self,
                 name=None,
                 theme=None,
                 type_of_announcement=None,
                 description=None,
                 location=None,
                 date_of_publication=None,
                 user_id=None):
        self.name = name
        self.theme = theme
        self.type_of_announcement = type_of_announcement
        self.description = description
        self.location = location
        self.date_of_publication=date_of_publication
        self.user_id = user_id
