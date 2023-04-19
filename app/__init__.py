from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask_migrate import Migrate

# создание объектов приложения и базы данных
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testdrive123@localhost:5432/testdrive'
app.config['SECRET_KEY'] = 'Adjgsdg234gjalfbcvDSF;m234:Fk-34-99841f..s#@$'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


login_manager = LoginManager(app)
