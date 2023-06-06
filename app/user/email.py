import json
import time
from threading import Thread

import pika
from flask import render_template, current_app
from flask_mail import Message

from app import mail
from app.models import ResetPasswordStatic
from config import Config


# async send message, but don`t work on pythonanywhere
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# this func must get whole request about email
def send_email(subject, sender, recipients, body, attachments=None):
    msg = Message(subject, sender=sender, recipients=recipients, body=body)

    if attachments is not None:
        attach_photo = attachments.split('/')[-1]
        with current_app.open_resource(attachments) as fp:
            msg.attach(attach_photo, 'image/png', fp.read())
    mail.send(msg)

    # Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):
    token = ResetPasswordStatic.get_reset_password_token(user)
    body = render_template('user/reset_password_email.html', user=user, token=token)
    send_email('Reset_password', Config.MAIL_USERNAME, [user.email], body)


# use rabbitmq queue for send message to email
def add_to_queue_email(subject, sender, recipients, body, attachments):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(
        {'subject': subject, 'sender': sender, 'recipients': recipients, 'body': body, 'attachments': attachments}))
    connection.close()
