from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, request
from functools import wraps
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from database import db
from Email import Email, bcrypt
import smtplib
import jwt


program = Flask(__name__)
program.secret_key = 'Some secret key'
program.config['SECRET_KEY'] = 'super-secret'
program.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
program.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

program.config['MAIL_SERVER'] = "smtp.gmail.com"
program.config['MAIL_PORT'] = 465
program.config['MAIL_USERNAME'] = "geoclock.app@gmail.com"
program.config['MAIL_PASSWORD'] = "GeoClock.app2021"
program.config['MAIL_USE_TLS'] = False
program.config['MAIL_USE_SSL'] = True

Email.init_app(program)
db.init_app(program)
bcrypt.init_app(program)


migrate = Migrate(program, db)

manager = Manager(program)
manager.add_command('db', MigrateCommand)

from models.user import User


def token_required(f):
    @wraps(f)
    def tokens(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify(message="Token is missing!!", status=200)
        #try:
        data = jwt.decode(token, program.config['SECRET_KEY'])
        current_user = User.query.filter_by(id=data['id']).first()
        if not current_user:
            print("Error")
            return "ERROR"
        #except:
            #return jsonify(message=token + " Token is invalid!!!", status=401)
        return f(current_user, *args, **kwargs)

    return tokens


from routes import announcement_routes, user_routes
"""server = WSGIServer(('127.0.0.1', 5000), program)
server.serve_forever()"""


if __name__ == '__main__':
    program.run()
