import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, '..', 'webapp.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'A0tr43j/3yO VB~XHH123!jmN42]pWpWX/,?RT!'
