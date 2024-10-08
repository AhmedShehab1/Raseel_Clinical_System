# flake8: noqa
from flask import Flask, session, request, current_app
from flask_mail import Mail
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch

# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
import logging
import pretty_errors
import os

pretty_errors.activate()

mail = Mail()
moment = Moment()
db = SQLAlchemy()  # This is the database engine
migrate = Migrate(db)  # This is the migration engine
babel = Babel()
login_manager = LoginManager()  # This is the login manager
login_manager.login_view = "login"
login_manager.login_message = _l("Please log in to access this page.")
# limiter = Limiter(
#     key_func=get_remote_address,
#     default_limits=['10 per minute'],
# )


def get_locale():
    return request.accept_languages.best_match(current_app.config["LANGUAGES"])


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.elasticsearch = (
        Elasticsearch([app.config["ELASTICSEARCH_URL"]])
        if app.config["ELASTICSEARCH_URL"]
        else None
    )
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    login_manager.init_app(app)
    # limiter.init_app(app)

    from web_flask.main import bp as main_bp
    from web_flask.errors import bp as errors_bp
    from web_flask.doctor_bp import doctor_bp
    from web_flask.auth import bp as auth_bp
    from web_flask.cli import bp as cli_bp
    from api.v1.views import bp as api_bp
    from web_flask.receptionist_bp import receptionist_bp
    from web_flask.patient_bp import patient_bp
    from web_flask.admin_bp import bp as admin_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(cli_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(receptionist_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(admin_bp)

    if not app.debug and not app.testing:
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

    return app


from models.base_model import BaseModel
import models as m


@login_manager.user_loader
def load_user(user_id):
    user_type = session.get("user_type")
    if user_type:
        user_model = getattr(m, user_type)
        if user_model:
            return db.session.get(user_model, user_id)
    return None
