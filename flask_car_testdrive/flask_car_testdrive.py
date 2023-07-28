from flask import redirect, url_for
from config import DevelopmentConfig
from config import ProductionConfig
from app import create_app

# here change config
CONFIG = ProductionConfig

# нужно поменять домен для запуска этого сайта на store
# pull на сервер из ветки main

# test server
# CONFIG_TEST = 'https://tework123.ru/'

# test with new_app on localhost
CONFIG_TEST = 'new_app'

print(10)
app = create_app(CONFIG)


@app.route('/')
def index():
    return redirect(url_for('user.index'))
