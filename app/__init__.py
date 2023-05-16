import os
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for
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

# импорт и регистрация blueprint
from app.user import bp as bp_user

app.register_blueprint(bp_user, url_prefix='/user')

from app.admin import bp as bp_admin

app.register_blueprint(bp_admin, url_prefix='/admin')

from app.errors import bp as bp_errors

app.register_blueprint(bp_errors, url_prefix='/errors')

with app.app_context():
    # db.drop_all()
    # db.create_all()
    pass


# menu = [['Home', '/user'], ['Сar brands', '/user/show_brands'], ['Sing in', '/user/login'],
#         ['Registration', '/user/register']]


@app.route('/')
def index():
    return redirect(url_for('user.index'))
