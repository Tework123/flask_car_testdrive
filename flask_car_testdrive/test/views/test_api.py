import base64
import json
import os
from base64 import b64encode

import pytest
import requests


def to_json(response, type_test):
    if type_test == 'new_app':
        return response.get_json()
    else:
        return response.json()


def right_response(type_test, url, request, client, headers=None, body=None):
    if type_test == 'new_app':
        if request == 'post':
            response = client.post(url, json=body, headers=headers)
            return response
        if request == 'get':
            response = client.get(url, json=body, headers=headers)
            return response
        if request == 'patch':
            response = client.patch(url, json=body, headers=headers)
            return response
        if request == 'delete':
            response = client.delete(url, json=body, headers=headers)
            return response
    else:
        if request == 'post':
            response = requests.post(type_test + url, json=body, headers=headers)
            return response

        if request == 'get':
            response = requests.get(type_test + url, json=body, headers=headers)
            return response

        if request == 'patch':
            response = requests.patch(type_test + url, json=body, headers=headers)
            return response

        if request == 'delete':
            response = requests.delete(type_test + url, json=body, headers=headers)
            return response


@pytest.mark.usefixtures('client', 'type_test')
class TestRegisterErrors:

    @pytest.mark.parametrize("test_input, expected_error_description, expected_status_code", [
        ({"name": "grisha",
          "email": "postgresmail.ru",
          "country": "usa",
          "password": "12353",
          "phone": "9193913293"}, 'email incorrect', 400),
        ({"name": "grisha",
          "email": "postgres@mail.ru",
          "country": "usa",
          "password": "1233",
          "phone": "9193913293"}, 'password length: 5-24, number must be', 400),
        ({"name": "gri",
          "email": "postgres@mail.ru",
          "country": "usa",
          "password": "12353",
          "phone": "9193913293"}, 'name length: 4-24', 400),
        ({"name": "gri",
          "email": "postgres@mail.ru",
          "country": "usa",
          "password": "12353",
          "phone": "91939913293"}, 'incorrect phone number', 400),
        ({"name": "grisha",
          "country": "usa",
          "password": "12353",
          "phone": "9193913293"}, 'register user error, not found some fields', 400)
    ])
    def test_registration_app(self, client, test_input, expected_error_description, expected_status_code, type_test):
        url = 'api/create_user'

        response = right_response(type_test, client=client, url=url, request='post',
                                  body=test_input)

        assert response.status_code == expected_status_code
        assert to_json(response, type_test)['error_place'] == 'Api error'
        assert to_json(response, type_test)['error_type'] == 'User error'
        assert to_json(response, type_test)['error_description'] == expected_error_description


@pytest.mark.usefixtures('client', 'context', 'type_test')
class TestRegLogTokenGet:

    def test_create_user(self, client, type_test):
        body = {"name": "grisha",
                "email": "postgres@mail.ru",
                "country": "usa",
                "password": "12353",
                "phone": "9193913293"}

        url = 'api/create_user'

        response = right_response(type_test, client=client, url=url, request='post',
                                  body=body)

        assert response.status_code == 200
        assert to_json(response, type_test)['data'] == 'registration success'

    def test_login(self, client, type_test):
        body = {"email": "postgres@mail.ru",
                "password": "12353"}

        url = 'api/login'
        response = right_response(type_test, client=client, url=url, request='post',
                                  body=body)
        assert response.status_code == 200
        assert to_json(response, type_test)['data'] == 'login success'

    def test_get_token(self, client, type_test, context):
        credentials = b64encode(b"postgres@mail.ru:12353").decode('utf-8')
        headers = {"Authorization": f"Basic {credentials}"}

        url = 'api/tokens'
        response = right_response(type_test, client=client, url=url, request='get',
                                  body=None, headers=headers)

        assert response.status_code == 200

        context['token'] = to_json(response, type_test)['token']

    def test_get_users(self, client, type_test, context):
        headers = {
            'Authorization': f'Bearer {context["token"]}'
        }
        url = 'api/get_users'
        response = right_response(type_test, client=client, url=url, request='get',
                                  body=None, headers=headers)

        assert response.status_code == 200
        assert to_json(response, type_test)['data'] != [{'email': 'postgres@mail.ru',
                                                         'id_user': 1,
                                                         'last_seen': to_json(response, type_test)['data'][0][
                                                             'last_seen'],
                                                         'name': 'grisha'}]


@pytest.mark.usefixtures('client', 'type_test')
class TestLoginErrors:
    @pytest.mark.parametrize("test_input, expected_error_description, expected_status_code", [
        ({"email": "postgres00@mail.ru",
          "password": "12353"}, 'this user don`t exist', 400),
        ({"email": "postgres@mail.ru",
          "password": "1233"}, 'password wrong', 400)])
    def test_login_errors(self, client, type_test, test_input, expected_error_description, expected_status_code):
        url = 'api/login'
        response = right_response(type_test, client=client, url=url, request='post',
                                  body=test_input, headers=None)
        assert response.status_code == expected_status_code
        assert to_json(response, type_test)['error_place'] == 'Api error'
        assert to_json(response, type_test)['error_type'] == 'User error'
        assert to_json(response, type_test)['error_description'] == expected_error_description


@pytest.mark.usefixtures('client', 'context', 'type_test', 'add_data_to_db')
class TestCommandGetCars:

    # token из прошлого класса тестов
    def test_get_cars(self, client, type_test, context):
        headers = {
            'Authorization': f'Bearer {context["token"]}'
        }

        url = 'api/get_cars'
        response = right_response(type_test, client=client, url=url, request='get',
                                  body=None, headers=headers)

        assert to_json(response, type_test)['data'] == [
            {'description': 'Price: 4 000 000, Power: 200 hp, Top Speed: 250 kmph, '
                            '0-100kmph: 6,8 seconds, Weight: 1740 kg, Price test drive: '
                            '5000',
             'name_car': 'Audi A6'},
            {'description': 'Price: 5 000 000, Power: 220 hp, Top Speed: 250 kmph, '
                            '0-100kmph: 6,3 seconds, Weight: 1840 kg, Price test drive: '
                            '6000',
             'name_car': 'Audi A7'},
            {'description': 'Price: 6 000 000, Power: 330 hp, Top Speed: 230 kmph, '
                            '0-100kmph: 6,1 seconds, Weight: 1960 kg, Price test drive: '
                            '7000',
             'name_car': 'Audi Q7'},
            {'description': 'Price: 3 000 000, Power: 140 hp, Top Speed: 220 kmph, '
                            '0-100kmph: 8,7 seconds, Weight: 1440 kg, Price test drive: '
                            '3000',
             'name_car': 'BMW 2'},
            {'description': 'Price: 6 000 000, Power: 240 hp, Top Speed: 260 kmph, '
                            '0-100kmph: 6,3 seconds, Weight: 1790 kg, Price test drive: '
                            '6000',
             'name_car': 'BMW 6'},
            {'description': 'Price: 3 500 000, Power: 160 hp, Top Speed: 200 kmph, '
                            '0-100kmph: 9,7 seconds, Weight: 1890 kg, Price test drive: '
                            '4000',
             'name_car': 'BMW X2'},
            {'description': 'Price: 2 500 000, Power: 130 hp, Top Speed: 220 kmph, '
                            '0-100kmph: 11,0 seconds, Weight: 1740 kg, Price test drive: '
                            '2500',
             'name_car': 'KIA CEED'},
            {'description': 'Price: 3 000 000, Power: 130 hp, Top Speed: 220 kmph, '
                            '0-100kmph: 9,7 seconds, Weight: 1540 kg, Price test drive: '
                            '3000',
             'name_car': 'KIA RIO'},
            {'description': 'Price: 7 000 000, Power: 340 hp, Top Speed: 230 kmph, '
                            '0-100kmph: 7,7 seconds, Weight: 2140 kg, Price test drive: '
                            '7000',
             'name_car': 'KIA Sportage'},
            {'description': 'Price: 10 000 000, Power: 380 hp, Top Speed: 280 kmph, '
                            '0-100kmph: 4,0 seconds, Weight: 1240 kg, Price test drive: '
                            '12000',
             'name_car': 'Porsche carrera 911'},
            {'description': 'Price: 5 000 000, Power: 310 hp, Top Speed: 240 kmph, '
                            '0-100kmph: 6,7 seconds, Weight: 1950 kg, Price test drive: '
                            '6000',
             'name_car': 'Porsche cayenne'},
            {'description': 'Price: 11 000 000, Power: 400 hp, Top Speed: 300 kmph, '
                            '0-100kmph: 5,0 seconds, Weight: 1440 kg, Price test drive: '
                            '13000',
             'name_car': 'Porsche taycan'},
            {'description': 'Price: 21 000 000, Power: 720 hp, Top Speed: 330 kmph, '
                            '0-100kmph: 2,9 seconds, Weight: 1260 kg, Price test drive: '
                            '20000',
             'name_car': 'f8-spider'},
            {'description': 'Price: 18 000 000, Power: 700 hp, Top Speed: 320 kmph, '
                            '0-100kmph: 3,0 seconds, Weight: 1340 kg, Price test drive: '
                            '18000',
             'name_car': 'f8-tributo'},
            {'description': 'Price: 17 000 000, Power: 620 hp, Top Speed: 320 kmph, '
                            '0-100kmph: 3,4 seconds, Weight: 1420 kg, Price test drive: '
                            '17000',
             'name_car': 'Ferrari roma'}]

    # в это фласк приложения нужно тоже фото загрузить, но как - непонятно, если нужно будет для сервера - настроим
    # @pytest.mark.skip
    def test_get_image_cars(self, client, context, type_test):
        headers = {
            'Authorization': f'Bearer {context["token"]}'
        }

        url = 'api/get_image_cars'
        response = right_response(type_test, client=client, url=url, request='get',
                                  body=None, headers=headers)

        images = to_json(response, type_test)['data']

        count = 0
        for i in range(len(images)):
            imgdata = base64.b64decode(images[i])
            filename = str(i) + '.jpg'  # I assume you have a way of picking unique filenames
            with open(filename, 'wb') as f:
                f.write(imgdata)
            count += 1
        if count == 45:
            for j in range(count):
                file = str(j) + '.jpg'
                os.remove(file)
        assert count == 45


@pytest.mark.usefixtures('client', 'context', 'type_test', 'add_data_to_db')
class TestEditUser:

    @pytest.mark.parametrize("test_input, expected_error_description, expected_status_code", [
        ({"email": "postgresmail.ru"}, 'email incorrect', 400),
        ({"password": "1234"}, 'password length: 5-24, number must be', 400),
        ({"name": "gri"}, 'name length: 4-24', 400),
        ({"phone": "91939913293"}, 'incorrect phone number', 400)
    ])
    def test_edit_field_user(self, client, type_test, context, test_input, expected_error_description,
                             expected_status_code):
        headers = {
            'Authorization': f'Bearer {context["token"]}'
        }
        url = 'api/edit_user'
        response = right_response(type_test, client=client, url=url, request='patch',
                                  body=test_input, headers=headers)

        assert response.status_code == expected_status_code
        assert to_json(response, type_test)['error_place'] == 'Api error'
        assert to_json(response, type_test)['error_type'] == 'User error'
        assert to_json(response, type_test)['error_description'] == expected_error_description


@pytest.mark.usefixtures('client', 'context', 'type_test', 'add_data_to_db')
class TestDeleteTokenUser:

    def test_delete_token(self, client, type_test, context):
        headers = {
            'Authorization': f'Bearer {context["token"]}'
        }

        url = 'api/tokens'
        response = right_response(type_test, client=client, url=url, request='delete',
                                  body=None, headers=headers)

        assert response.status_code == 200
        assert to_json(response, type_test)['data'] == 'token has been deleted'

    def test_get_token(self, client, type_test, context):
        credentials = b64encode(b"postgres@mail.ru:12353").decode('utf-8')

        headers = {"Authorization": f"Basic {credentials}"}

        url = 'api/tokens'
        response = right_response(type_test, client=client, url=url, request='get',
                                  body=None, headers=headers)
        assert response.status_code == 200
        context['token'] = to_json(response, type_test)['token']

    def test_delete_user(self, client, type_test, context):
        headers = {
            'Authorization': f'Bearer {context["token"]}'
        }
        url = 'api/delete_user'
        response = right_response(type_test, client=client, url=url, request='delete',
                                  body=None, headers=headers)
        assert response.status_code == 200
        assert to_json(response, type_test)['data'] == 'user has been deleted'
