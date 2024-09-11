from flask import render_template, current_app
from web_flask import mail
from flask_mail import Message
from threading import Thread


def send_email_async(app, msg):
    """
    Send email asynchronously
    Args:
        app : Flask app
        msg : Message object
    """
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """
    Send email
    Args:
        subject (str): Email subject
        sender       : Email sender
        recipients   : Email recipients
        text_body    : Email text body
        html_body    : Email html body
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_email_async, args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):
    """
    Send password reset email
    Args:
        user: User object
    """
    token = user.get_reset_password_token()
    send_email(
        "[Raseel Medical Center] Reset Your Password",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )
