import os

from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

# создание объектов приложения и базы данных
app = Flask(__name__)
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = Config.SECRET_KEY
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

# config for mail.send(msg)
app.config['MAIL_SERVER'] = Config.MAIL_SERVER
app.config['MAIL_PORT'] = int(Config.MAIL_PORT)
app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD

mail = Mail(app)

# config for SMTP logging
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
file_handler = RotatingFileHandler('logs/log_test.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

# action to logs/log.log
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

# action to email
mail_handler.setLevel(logging.ERROR)
app.logger.addHandler(mail_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Start application')
