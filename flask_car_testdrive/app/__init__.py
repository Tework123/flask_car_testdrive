import os

import pika
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app
from flask_migrate import Migrate
from rq import Queue

from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from redis import Redis

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

redis = Redis.from_url(os.environ.get('REDIS_URL_LOCAL'))
task_queue = Queue(connection=redis)


# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()
# channel.queue_declare(queue='hello')


def create_app(config):
    # создание объектов приложения и базы данных
    app = Flask(__name__)

    # берет все конфиги из класса Config и заносит в приложение flask
    app.config.from_object(config)

    # без сортировки возвращаемых jsonfy
    app.json.sort_keys = False

    # подключаем все модули
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    # redis = Redis.from_url(config.REDIS_URL)
    # app.task_queue = Queue(connection=redis)

    mail_handler = SMTPHandler(mailhost=(Config.MAIL_SERVER, int(Config.MAIL_PORT)),
                               fromaddr=Config.MAIL_USERNAME,
                               toaddrs=Config.ADMINS,
                               subject='Error flask_test_drive',
                               credentials=(Config.MAIL_USERNAME, Config.MAIL_PASSWORD),
                               secure=()
                               )

    # for SMTP logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/log_test.log', maxBytes=10240, backupCount=1)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

    # action to logs/log.log
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

    # action to email
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    app.logger.setLevel(logging.ERROR)

    # импорт и регистрация blueprint in context flask_app

    with app.app_context():
        from app.user import bp as bp_user

        app.register_blueprint(bp_user, url_prefix='/user')

        from app.admin import bp as bp_admin

        app.register_blueprint(bp_admin, url_prefix='/admin')

        from app.api import bp as bp_api

        app.register_blueprint(bp_api, url_prefix='/api')

        from app.errors import bp as bp_errors

        app.register_blueprint(bp_errors)

        from app.command import bp as bp_command

        app.register_blueprint(bp_command)

    return app
