import datetime
import json
import time

import pytz
from flask import render_template, jsonify, request, flash
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import ApiAuthError
from app.models import Users, Cars, Reviews
from app.user.email import send_email
from flask_car_testdrive import CONFIG

menu = [['Home', '/user'], ['Сar brands', '/user/show_brands'], ['Sing in', '/user/login'],
        ['Registration', '/user/register'], ['Api', '/api']]


# обработать все апишки так, как должно быть на реальном проекте везде, куча raise и except с пояснениями
# добавить новые классы ошибок, не только error_authenticated

# сделать разные виды запросов, делете, пост, и тд

# проверить все это на докере

# у меня в закладках апи авто сайтов, может оттуда вытащить что-нибудь
# также несколько ручек прикрутить, поиграться так сказать с json
# тестирование апи тоже написать, посмотреть сначала как это делают

# надо бы тестирование получше сделать
# далее хост на платный сервак с помощью докера

# поиграться со скоростью запросов в базу данных, учитывая видосы по оптимизированию

# поиграть с react js и flask по мигелю

# поиграть с ооп и переходить на джанго

@bp.route('/', methods=['POST', 'GET'])
def index():
    whole_api_routes = ['get_users', 'get_cars', 'get_reviews/name_car']
    get_users_example = 123
    return render_template('api/index.html', main_menu=menu, title='api',
                           whole_api_routes=whole_api_routes, get_users_example=get_users_example)


@bp.route('/get_users_example', methods=['GET'])
def get_users_example():
    user_dict = db.session.query(Users.id_user, Users.country, Users.last_seen_profile).limit(5).all()
    users_dict = []

    for row in user_dict:
        row = {'id_user': row.id_user, 'country': row.country,
               'last_seen': row.last_seen_profile}
        users_dict.append(row)

    return jsonify({'data': users_dict})


@bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()

    if not Users.query.filter_by(email=data['email']).first():
        hash = generate_password_hash(data['password'])
        user = Users(name=data['name'], password=hash, email=data['email'],
                     country=data['country'], phone=data['phone'])
        db.session.add(user)
        db.session.flush()
        db.session.commit()

        subject = 'You was register on testdrive'
        body = user.name + ' Welcome!'
        send_email(subject, CONFIG.MAIL_USERNAME, [user.email], body)
        #
        #
        #         except:
        #             db.session.rollback()
        #             flash('incorrect data', category='error')
        return jsonify({'data': 'register success'})
    else:
        return jsonify({'data': 'this email already register'})

        # return jsonify({'data': 'some mistake appear'})

    return jsonify({'data': 'register error'})


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db.session.query(Users).filter_by(email=data['email']).first()
    check_password = check_password_hash(user.password, data['password'])
    if check_password:
        login_user(user)
        return jsonify({'data': 'login success'})
    return jsonify({'data': 'login error'})


@bp.route('/get_users', methods=['GET'])
@token_auth.login_required
def get_users():
    try:
        users = db.session.query(Users.id_user, Users.name, Users.email, Users.last_seen_profile).all()
        x = 1 / 0
        if users:
            # users_dict = [tuple(row) for row in users]
            users_dict = []
            for row in users:
                row = {'id_user': row.id_user, 'name': row.name, 'email': row.email,
                       'last_seen': row.last_seen_profile}
                users_dict.append(row)
    except Exception as e:
        raise ApiAuthError('Some mistake men', str(e), 404)
    return jsonify({'data': users_dict})


@bp.route('/get_cars', methods=['GET'])
@token_auth.login_required
def get_cars():
    cars = db.session.query(Cars.name_car, Cars.description).all()
    cars_dict = []
    for row in cars:
        row = {'name_car': row.name_car, 'description': row.description}
        cars_dict.append(row)

    return jsonify({'data': cars_dict})


@bp.route('/get_reviews/<name_car>', methods=['GET'])
@token_auth.login_required
def get_reviews(name_car):
    reviews = db.session.query(Reviews.date, Reviews.text, Reviews.degree).join(Cars,
                                                                                Reviews.id_car == Cars.id_car).where(
        Cars.name_car == name_car).all()

    reviews_dict = []
    for row in reviews:
        row = {'date': row.date, 'text': row.text, 'dergee': row.degree}
        reviews_dict.append(row)

    return jsonify({'data': reviews_dict})
