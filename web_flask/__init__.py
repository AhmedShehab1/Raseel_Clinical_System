# flake8: noqa
from flask import Flask
from config import Config
import pretty_errors
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)  # This is the database engine
migrate = Migrate(app, db)  # This is the migration engine

login_manager = LoginManager() # This is the login manager
login_manager.init_app(app)
login_manager.login_view = 'login'

from web_flask import routes
from models.base_model import BaseModel
import models as m

@login_manager.user_loader
def load_patient(patient_id):
    return db.session.get(m.Patient, patient_id)
