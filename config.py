import os	

secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
PWD = os.path.abspath(os.curdir)	

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/mydatabase.db'.format(PWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False
