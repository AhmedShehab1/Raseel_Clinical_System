from api.v1.views import bp
from flask import request, current_app, render_template
from api.v1.errors import bad_request

# from web_flask import limiter
from web_flask.auth.email import send_email


@bp.post("/sendEmail")
# @limiter.limit("3 per hour")
def sendEmail():
    data = request.get_json()
    if (
        "name" not in data
        or "email" not in data
        or "phone" not in data
        or "msg" not in data
    ):
        return bad_request("Missing required fields")

    error = send_email(
        "New Visitor Message",
        current_app.config["MAIL_DEFAULT_SENDER"],
        current_app.config["ADMINS"],
        render_template("email/visitor_msg.txt", data=data),
        render_template("email/visitor_msg.html", data=data),
    )
    if error:
        return error

    return "success", 200
