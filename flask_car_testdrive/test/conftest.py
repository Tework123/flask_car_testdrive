from app import create_app
from app import db
from config import TestingConfig
import pytest


@pytest.fixture(scope='session', autouse=True)
def app():
    # before test
    _app = create_app(TestingConfig)
    app_context = _app.app_context()
    app_context.push()
    yield _app

    # then end session
    db.session.remove()
    db.drop_all()
    app_context.pop()
