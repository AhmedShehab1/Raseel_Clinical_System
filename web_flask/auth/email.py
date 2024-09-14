from flask import render_template, current_app, jsonify
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
        try:
            mail.send(msg)
        except Exception as e:
            current_app.logger.error(f"Error sending email: {str(e)}")


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
    try:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        Thread(target=send_email_async, args=(current_app._get_current_object(), msg)).start()
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return jsonify({"error": "Failed to send email"}), 500

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

def send_admin_review_email(user):
    """
    Send admin review email
    Args:
        data: Registration data
    """
    token = user.get_approve_request_token()
    send_email(
        "[Raseel Medical Center] Account Review",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=current_app.config["ADMINS"],
        text_body=render_template("email/admin_review.txt", data=user, token=token),
        html_body=render_template("email/admin_review.html", data=user, token=token),
    )
