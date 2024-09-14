from flask import render_template, flash
from web_flask import db
from flask_babel import _
from web_flask.errors import bp


@bp.app_errorhandler(404)
def page_not_found(error):
    flash(_("Page not found"), "danger")
    return render_template("404.html"), 404


@bp.app_errorhandler(500)
def server_error(error):
    flash(_("An unexpected error has occured"), "danger")
    db.session.rollback()
    return render_template("500.html"), 500
