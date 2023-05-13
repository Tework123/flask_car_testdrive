from threading import Thread

from flask import render_template, current_app
from flask_mail import Message

from app import mail
from app.models import ResetPasswordStatic
from config import Config


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, body):
    msg = Message(subject, sender=sender, recipients=recipients, body=body)
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):
    token = ResetPasswordStatic.get_reset_password_token(user)

    body = render_template('user/reset_password_email.html', user=user, token=token)
    send_email('Reset_password', Config.MAIL_USERNAME, [user.email], body)
