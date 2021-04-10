from database import db
from re import *
from .saved_announcements import Saved


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    hash_code = db.Column(db.String(120))
    saved_announcement = db.relationship('Saved', backref='user')

    def __init__(self,
                 user_name=None,
                 first_name=None,
                 last_name=None,
                 email=None,
                 password=None,
                 hash_code=None):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.hash_code = hash_code
        self.email = email
        self.password = password

    def Any_Empty_Field(self):
        if not self.user_name:
            return True
        if not self.first_name:
            return True
        if not self.last_name:
            return True
        if not self.email:
            return True
        if not self.password:
            return True
        return False


    def Invalid_Data(self):
        name = compile('(^|\s)(\w){2,30}(\s|$)')
        email = compile('(^|\s)[-a-z|0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
        if not name.match(self.user_name):
            return True
        if not name.match(self.first_name):
            return True
        if not name.match(self.last_name):
            return True
        if not email.match(self.email):
            return True
        return False

    @classmethod
    def Get_from_db(self, user_id=None, user_name=None, email=None):
        if user_id:
            return User.query.filter_by(id=user_id).first()
        if user_name:
            return User.query.filter_by(user_name=user_name).first()
        if email:
            return User.query.filter_by(email=email).first()
        return None
