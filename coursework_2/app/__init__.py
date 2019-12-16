from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

from app import views, models
