from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50),  nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    list_of_announcements = db.relationship('Announcement', backref='creator')


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),  nullable=False)
    theme = db.Column(db.String(50), nullable=False)
    type_of_announcement = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    date_of_publication = db.Column(db.DATETIME, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
