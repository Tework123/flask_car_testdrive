from flask import redirect, url_for
from config import DevelopmentConfig
from config import ProductionConfig
from config import TestingConfig
from app import create_app

# here change config
CONFIG = DevelopmentConfig

# test with new_app or localhost, docker, server
CONFIG_TEST = 'new_app'

app = create_app(CONFIG)


@app.route('/')
def index():
    return redirect(url_for('user.index'))
