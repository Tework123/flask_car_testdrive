from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

menu = [['Home', 'http://127.0.0.1:5000/'], ['Сar brands', 'http://127.0.0.1:5000/user/show_brands'],
        ['Sing in', 'login'],
        ['Registration', 'register'], ['Api', 'http://127.0.0.1:5000/api']]
from . import routes

# в микросервис выносим авторизацию, регистрацию, профиль и все остальное связанное с ним
# надо первую базу почистить от юзера, а то он по регистрирует во второй базе на id = 1,
# переходит на старый порт и достает пользователя с id=1 , а там другой,)))
