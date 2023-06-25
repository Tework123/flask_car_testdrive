import base64
import json
import os
import time

from flask import render_template, jsonify, request
from flask_login import current_user, login_user
from jsonschema.validators import validate
from werkzeug.security import generate_password_hash, check_password_hash

# решить проблему с циркуляркой при тестах
# from app.user.email import send_email

from app import db, redis
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import ApiDbError, ApiUserError
from app.api.schemas import schema_get_users_example
from app.api.validation import UserFieldValidation
from app.models import Users, Cars, Reviews, Photos
from flask_car_testdrive import CONFIG

menu = [['Home', '/user'], ['Сar brands', '/user/show_brands'], ['Sing in', '/user/login'],
        ['Registration', '/user/register'], ['Api', '/api']]



# если опять будет атака на редис, то использовать пароль в конфиге

# в докере сделать один образ для создания автоматического бекапов базы
# потренить как ручное восстановление базы, так и через этот образ

# сделать сайт https

# протестить загрузку new кода через докерхаб

# изучить gitlab и ic\dc

# нагрузочное тестирование через библиотеку, наверное в отдельной папке pytest либо вообще отдельно


# поиграться со скоростью запросов в базу данных, учитывая видосы по оптимизации

# поиграть с react js и flask по мигелю

# поиграть с ооп и переходить на джанго


def to_dict(data, fields):
    list_dicts = []

    for i in range(len(data)):
        data_dict = {}
        for j in range(len(fields)):
            data_dict[fields[j]] = data[i][j]
        list_dicts.append(data_dict)

    return list_dicts


@bp.route('/', methods=['POST', 'GET'])
def index():
    whole_api_routes = ['get_users', 'get_cars', 'get_reviews/name_car']
    get_users_example = 'user'
    return render_template('api/index.html', main_menu=menu, title='api',
                           whole_api_routes=whole_api_routes, get_users_example=get_users_example)


@bp.route('/get_users_example', methods=['GET'])
def get_users_example():
    try:
        users = db.session.query(Users.id_user, Users.country, Users.last_seen_profile).limit(5).all()
    except Exception as e:
        raise ApiDbError('user example', str(e), 500)

    users_dict = []
    if users:
        for row in users:
            row = {'id_user': row.id_user, 'country': row.country,
                   'last_seen': row.last_seen_profile}
            users_dict.append(row)

    response = jsonify({'data': users_dict})
    response.status_code = 200
    validate(instance=response.get_json(), schema=schema_get_users_example)
    return response


@bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()

    try:
        fields = data['email'], data['password'], data['name'], data['phone']
    except Exception as e:
        raise ApiUserError('register user error, not found some fields', str(e), 400)

    UserFieldValidation(data['email']).email_validation()
    UserFieldValidation(data['password']).password_validation()
    UserFieldValidation(data['phone']).phone_validation()
    UserFieldValidation(data['name']).name_validation()

    hash = generate_password_hash(data['password'])
    try:
        user = Users(name=data['name'], password=hash, email=data['email'],
                     country=data['country'], phone=data['phone'])
        db.session.add(user)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        raise ApiDbError('register user error', str(e), 500)

    subject = 'You was register on testdrive'
    body = user.name + ' Welcome!'

    # не думаю, что нужно сообщать пользователям, что модуль отправки приветственных писем сломался
    # send_email(subject, CONFIG.MAIL_USERNAME, [user.email], body)

    response = jsonify({'data': 'registration success'})
    response.status_code = 200
    return response


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = db.session.query(Users).filter_by(email=data['email']).first()
    if not user:
        raise ApiUserError('this user don`t exist', 400)

    check_password = check_password_hash(user.password, data['password'])
    if not check_password:
        raise ApiUserError('password wrong', 400)

    login_user(user)

    response = jsonify({'data': 'login success'})
    response.status_code = 200
    return response


@bp.route('/delete_user', methods=['DELETE'])
@token_auth.login_required
def delete_user():
    if token_auth.current_user().profile_pic:
        file_path = CONFIG.basepath + 'app/static/profile_image/' + token_auth.current_user().profile_pic
        if os.path.exists(file_path):
            os.remove(file_path)

    Users.query.filter_by(id_user=token_auth.current_user().id_user).delete()
    db.session.commit()

    return jsonify({'data': 'user has been deleted'})


@bp.route('/edit_user', methods=['PUT'])
@token_auth.login_required
def edit_user():
    data = request.get_json()
    user = token_auth.current_user()

    if not user:
        raise ApiUserError('this user don`t exist', 400)

    UserFieldValidation(data['email']).email_validation()
    UserFieldValidation(data['password']).password_validation()
    UserFieldValidation(data['phone']).phone_validation()
    UserFieldValidation(data['name']).name_validation()

    hash = generate_password_hash(data['password'])

    user.name = data['name']
    user.password = hash
    user.email = data['email']
    user.country = data['country']
    user.phone = data['phone']
    db.session.commit()
    return jsonify({'data': f'edit profile for {user.email} success'})


@bp.route('/edit_user', methods=['PATCH'])
@token_auth.login_required
def edit_field_user():
    data = request.get_json()
    user = token_auth.current_user()

    if not user:
        raise ApiUserError('this user don`t exist', 400)

    # создаем словарь со старыми значениями для последующего сравнения
    user_data_old = {'email': user.email, 'password': 'old_password', 'phone': user.phone, 'country': user.country,
                     'name': user.name}

    # в цикле меняем False на значение, полученное от пользователя, если значения нет, то обрабатывается ошибка
    dict_fields = {'email': False, 'password': False, 'phone': False, 'country': False, 'name': False}

    for key in dict_fields.keys():
        try:
            dict_fields[key] = data[key]
        except KeyError:
            pass

    # проверка на правильность введенных данных, записываются в коммит, отправка в бд после проверки всех полей
    if dict_fields['email']:
        # создается экземпляр класса для проверки данных, если происходит ошибка,
        # то в коммит новые данные не записываются
        UserFieldValidation(dict_fields['email']).email_validation()
        user.email = dict_fields['email']

    if dict_fields['password']:
        UserFieldValidation(dict_fields['password']).password_validation()
        user.password = generate_password_hash(dict_fields['password'])
        dict_fields['password'] = '*' * (len(dict_fields['password']))

    if dict_fields['phone']:
        UserFieldValidation(dict_fields['phone']).phone_validation()
        user.phone = dict_fields['phone']

    if dict_fields['name']:
        UserFieldValidation(dict_fields['name']).name_validation()
        user.name = dict_fields['name']

    if dict_fields['country']:
        user.country = dict_fields['country']

    db.session.commit()

    # запись измененных полей
    changed = {}
    for key in dict_fields:
        if user_data_old[key] != dict_fields[key] and dict_fields[key]:
            changed[key] = user_data_old[key] + ' to ' + dict_fields[key]

    return jsonify({'data': f'edit fields {changed} success'})


@bp.route('/get_users', methods=['GET'])
@token_auth.login_required
def get_users():
    try:
        users = db.session.query(Users.id_user, Users.name, Users.email, Users.last_seen_profile).all()
    except Exception as e:
        raise ApiDbError('users', str(e), 500)

    users_dict = []
    if users:
        for row in users:
            row = {'id_user': row.id_user, 'name': row.name, 'email': row.email,
                   'last_seen': row.last_seen_profile}
            users_dict.append(row)

    return jsonify({'data': users_dict})


@bp.route('/get_cars', methods=['GET'])
@token_auth.login_required
def get_cars():
    cached_data_cars = redis.get('cars')
    if cached_data_cars:
        cars_dict = json.loads(cached_data_cars)
    else:
        try:
            cars = db.session.query(Cars.name_car, Cars.description).all()
            cars_dict = []
            if cars:
                cars_dict = to_dict(cars, ['name_car', 'description'])
        except Exception as e:
            raise ApiDbError('cars', str(e), 500)

        redis.setex('cars', 20, json.dumps(cars_dict))

    response = jsonify({'data': cars_dict})
    return response


@bp.route('/get_reviews/<name_car>', methods=['GET'])
@token_auth.login_required
def get_reviews(name_car):
    try:
        reviews = db.session.query(Reviews.date, Reviews.text, Reviews.degree).join(Cars,
                                                                                    Reviews.id_car == Cars.id_car).where(
            Cars.name_car == name_car).all()
    except Exception as e:
        raise ApiDbError('reviews', str(e), 500)

    reviews_dict = []
    if reviews:
        for row in reviews:
            row = {'date': row.date, 'text': row.text, 'degree': row.degree}
            reviews_dict.append(row)

    return jsonify({'data': reviews_dict})


@bp.route('/get_image_cars', methods=['GET', 'HEAD'])
@token_auth.login_required
def get_image_cars():
    try:
        cars_images = db.session.query(Photos.name_photo).all()
    except Exception as e:
        raise ApiDbError('cars_images error', str(e), 500)

    cars_images_dict = []

    if cars_images:
        # превращает список row в список элементов
        cars_images_dict = [tuple(row)[0] for row in cars_images]

    str_images = []
    for i in cars_images_dict:
        file_path = CONFIG.basepath + 'app/static/car_image/' + i

        # закрашенная функция отправляет картинки, прямо картинки, но очень не удобно обрабатывать их
        # a = send_file(file_path, as_attachment=False)

        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            image_str = encoded_string.decode(encoding='utf-8')

            str_images.append(image_str)
    response = jsonify({'data': str_images})
    response.headers['amount_cars_images'] = len(cars_images_dict)
    return response
