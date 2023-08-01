import pytest


@pytest.fixture(scope='session', autouse=True)
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def context():
    return {}
