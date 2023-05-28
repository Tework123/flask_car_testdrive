import os
import time

from rq import Queue

import app
from flask import render_template, current_app
from flask_mail import Message

from app import mail
from app.models import ResetPasswordStatic
from config import Config


# async send message, but don`t work on pythonanywhere
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)


def send_email(subject, sender, recipients, body, attachments=None):
    msg = Message(subject, sender=sender, recipients=recipients, body=body)

    if attachments is not None:
        attach_photo = attachments.split('/')[-1]
        with current_app.open_resource(attachments) as fp:
            msg.attach(attach_photo, 'image/png', fp.read())
    return mail.send(msg)

    # Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


# разбираем докер, постоянно вылазит, а я не понимаю, что происходит
# разбираем rabbitmq, подключаем и так далее, надо попробовать выкатить на платный хостинг, который это все поддерживает
# скорее всего не найдем такой, можно только с реббит и кешированием поиграть на реальном сервере и то это не точно
# поэтому используем конфиги для разделения версий приложения
# далее апи по мигелю и другим источникам, почитать побольше
# потом надо захостить это дерьмо на платный сервак за 140 рублей и администрировать, реально можно все установить

# нужен образ фласк приложения, образ постгрес, гуникорн и нгинкс тоже нужны, а также редис
# что делать с точкой входа не понятно, там какой bach файл от мигеля

def send_password_reset_email(user):
    token = ResetPasswordStatic.get_reset_password_token(user)
    body = render_template('user/reset_password_email.html', user=user, token=token)
    send_email('Reset_password', Config.MAIL_USERNAME, [user.email], body)


def new_func(user):
    time.sleep(2)
    print(user)
    return True


from redis import Redis


def send_test(user):
    # redis = Redis.from_url(os.environ.get('REDIS_URL_LOCAL'))
    # task_queue = Queue('tasks', connection=redis)
    task_queue.enqueue(new_func, user)


def add_to_queue_send_email(subject, sender, recipients, body, attachments=None):
    print(1)
    app.task_queue.enqueue(send_email, subject, sender, recipients, body, attachments)
    print(2)
    return 'send'
