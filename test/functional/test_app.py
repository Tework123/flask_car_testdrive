import pytest

from app.main import app


# def test_index():
#     response = app.test_client().get('/user/')
#     assert response.status_code == 200

@pytest.mark.usefixtures('db')
class TestBasic():
    def test_home(self, client):
        res = client.get('/')
        assert res.status_code == 200