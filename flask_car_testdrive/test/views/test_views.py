import json

import pytest


def test_view_login(client):
    response = client.get("user/login")
    assert response.status_code == 200


def test_view_register(client):
    response = client.post('/user/register', data=json.dumps(213))

    assert response.status_code == 200


@pytest.mark.usefixtures('client')
class TestViewsUsersPost:
    @pytest.mark.parametrize("test_input,expected", [
        ('/user/register', 200),
        ('/user/login', 200)
    ])
    def test_views_users_post(self, test_input, expected, client):
        response = client.post(test_input, data=json.dumps(213))
        assert response.status_code == expected


@pytest.mark.usefixtures('client')
class TestViewsUsersGet:
    @pytest.mark.parametrize("test_input,expected", [
        ('/user/register', 200),
        ('/user/login', 200),
        ('/user', 308)
    ])
    def test_views_users_get(self, test_input, expected, client):
        response = client.get(test_input)
        assert response.status_code == expected
