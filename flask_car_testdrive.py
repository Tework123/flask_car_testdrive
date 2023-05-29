from flask import redirect, url_for
from config import DevelopmentConfig
from config import ProductionConfig
from config import TestingConfig
from app import create_app

# here change config
CONFIG = DevelopmentConfig

app = create_app(CONFIG)


@app.route('/')
def index():
    return redirect(url_for('user.index'))
#удалить эти пайкеши
# понять что я сделал с этим токеном, пулом и конфигом ребазе
# далее найсраиваем докер, можно все это еще раз прокрутить, новый проект, либо просто докер папки
# выташить из этой основной папки и попробовать
