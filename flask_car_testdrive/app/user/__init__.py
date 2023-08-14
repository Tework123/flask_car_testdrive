from flask import Blueprint

bp = Blueprint('user', __name__, template_folder='templates', static_folder='static')

menu = [['Home', './'], ['Сar brands', 'show_brands'], ['Sing in', 'login'],
        ['Registration', 'register']]
from app.user import routes
