import pytest


@pytest.fixture(scope='session', autouse=True)
def client(app):
    return app.test_client()
