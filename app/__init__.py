from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from config import Config

# создание объектов приложения и базы данных
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = Config.SECRET_KEY

db = SQLAlchemy(app)
migrate = Migrate(app, db)



login_manager = LoginManager(app)
