from flask import redirect, url_for
from config import DevelopmentConfig
from config import ProductionConfig
from app import create_app

# here change config
import os

# set environment auto
if os.environ.get('ENV') == 'development':
    CONFIG = DevelopmentConfig()
else:
    CONFIG = ProductionConfig()


# test server
# CONFIG_TEST = 'https://tework123.ru/'

# test with new_app on localhost
CONFIG_TEST = 'new_app'

app = create_app(CONFIG)


@app.route('/')
def index():
    return redirect(url_for('user.index'))
