# flake8: noqa
from flask import Flask
from flask_mail import Mail
from config import Config
import pretty_errors
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_moment import Moment
from flask import request
from flask_babel import Babel, lazy_gettext as _l
import os

pretty_errors.activate()

app = Flask(__name__)
if os.getenv("FLASK_ENV") == "development":
    app.config.from_object("config.TestConfig")
else:
    app.config.from_object(Config)


mail = Mail(app)
moment = Moment(app)
db = SQLAlchemy(app)  # This is the database engine
migrate = Migrate(app, db)  # This is the migration engine

def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

from web_flask.main import bp as main_bp
from web_flask.errors import bp as errors_bp
from web_flask.doctor_bp import doctor_bp
from web_flask.auth import bp as auth_bp
app.register_blueprint(errors_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)




babel = Babel(app, locale_selector=get_locale)

if not app.debug:
    if app.config["MAIL_SERVER"]:
        auth = None
        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        secure = None
        if app.config["MAIL_USE_TLS"]:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr=app.config["MAIL_DEFAULT_SENDER"],
            toaddrs=app.config["ADMINS"],
            subject="Raseel Failure",
            credentials=auth,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/raseel.log", maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Raseel startup")

login_manager = LoginManager()  # This is the login manager
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = _l("Please log in to access this page.")

from models.base_model import BaseModel
import models as m


@login_manager.user_loader
def load_patient(patient_id):
    return db.session.get(m.Patient, patient_id)
