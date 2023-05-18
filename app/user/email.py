from flask import render_template
from flask_mail import Message

from app import mail, app
from app.models import ResetPasswordStatic
from config import Config


# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)


def send_email(subject, sender, recipients, body, attachments=None):
    msg = Message(subject, sender=sender, recipients=recipients, body=body)

    if attachments is not None:
        attach_photo = attachments.split('/')[-1]
        with app.open_resource(attachments) as fp:
            msg.attach(attach_photo, 'image/png', fp.read())
    mail.send(msg)

    # Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):
    token = ResetPasswordStatic.get_reset_password_token(user)
    print(token)

    body = render_template('user/reset_password_email.html', user=user, token=token)
    send_email('Reset_password', Config.MAIL_USERNAME, [user.email], body)
