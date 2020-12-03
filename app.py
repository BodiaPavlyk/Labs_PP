from gevent.pywsgi import WSGIServer
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from database import db


program = Flask(__name__)
program.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
program.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(program)

migrate = Migrate(program, db)

manager = Manager(program)
manager.add_command('db', MigrateCommand)


def db_create():
    db.create_all()


@program.route("/api/v1/hello-world-20")
def hello():
    return "Hello world! Варіант 20"


server = WSGIServer(('127.0.0.1', 5000), program)
server.serve_forever()


"""if __name__ == '__main__':
    program.run()
"""