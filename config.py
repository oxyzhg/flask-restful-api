import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DB_USER = 'root'
    DB_PASSWORD = '369nice'
    DB_HOST = 'localhost'
    DB_DB = 'flask-api'

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DB
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False