import os


WTF_CSRF_ENABLED = True
SECRET_KEY = "comp2011_cw2"


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tmp', 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
