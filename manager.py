from flask_script import Manager
from flask import app, db
from flask.models import *

manager = Manager(app)
app.config['DEBUG'] = True  # Ensure debugger will load.


@manager.command
def create_tables():
    "Create relational database tables."
    db.create_all()


@manager.command
def drop_tables():
    "Drop all project relational database tables. THIS DELETES DATA."
    db.drop_all()


@manager.command
def add_data_tables():
    db.create_all()
    war = Warriors()
    war.idwarrior = "3Jeh4L"
    war.os = "windows 7"
    war.arch = "32bit"
    war.name = "pruebas"
    war.pid = "3434"
    war.lastseen = DateTime()
    db.session.add(war)
    db.session.commit()



if __name__ == '__main__':
    manager.run()