# flake8: noqa
from flask import Flask
from config import Config
import pretty_errors
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)  # This is the database engine
migrate = Migrate(app, db)  # This is the migration engine

from web_flask import routes
from models.base_model import BaseModel
import models
