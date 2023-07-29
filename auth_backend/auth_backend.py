from flask import redirect, url_for
from config import DevelopmentConfig
from config import ProductionConfig
# from config import DevelopmentConfig
# from config import ProductionConfig
from auth_app import create_app

# here change config
CONFIG = DevelopmentConfig

# test server
# CONFIG_TEST = 'https://tework123.ru/'

# test with new_app on localhost
CONFIG_TEST = 'new_app'

app = create_app(CONFIG)


# @app.route('/')
# def index():
#     return redirect(url_for('user.index'))
