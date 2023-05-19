from flask import redirect, url_for

from app import create_app

app = create_app()


@app.route('/')
def index():
    return redirect(url_for('user.index'))


#
# Установить единорога и нгинкс, захостить и установить тоже самое на пайтоненивхере
#
# Попробовать снова пайтест или юниттесты от мигеля
# разобрать эти гребаные миграции
# redis and miguel
# FOR NEXT PROJECT:
# и разбирать этот говнокод, наладить нормальные url, посмотреть на других сайтах и sqlалхеми, какие запросы делать
# хранение сразу пути в базе данных для скорости
