from flask import redirect, url_for
from config import DevelopmentConfig
from config import ProductionConfig
from config import TestingConfig
from app import create_app

# here change config
CONFIG = ProductionConfig

# test server
CONFIG_TEST = 'http://45.141.76.71/'

# test with new_app on localhost
# CONFIG_TEST = 'new_app'

app = create_app(CONFIG)


@app.route('/')
def index():
    return redirect(url_for('user.index'))
