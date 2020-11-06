import os

basedir = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' +'mydatabase.db'
SQLALCHEMY_DATABASE_DIR =  'mydatabase.db'
SQLALCHEMY_DATABASE_VERSION =  2
CONSOLE_VERSION =  0.1
CONSOLE_PATH =  "consola"
SQLALCHEMY_TRACK_MODIFICATIONS= False
SQLALCHEMY_MIGRATE_REPO =  'db_repository'
APP_VERSION="0.2.1" 

