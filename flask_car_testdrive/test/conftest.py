from app import create_app
from app import db
from app.command.routes import add_user_base, add_brands_base, add_cars_base, add_reviews_base
from config import TestingConfig
import pytest
from flask_car_testdrive import CONFIG_TEST


@pytest.fixture(scope='session', autouse=True)
def type_test():
    if CONFIG_TEST == 'new_app':
        return 'new_app'
    else:
        return CONFIG_TEST


@pytest.fixture(scope='session', autouse=True)
def app():
    # before test
    _app = create_app(TestingConfig)
    app_context = _app.app_context()
    app_context.push()
    db.create_all()

    yield _app

    # after test end session
    db.session.remove()
    db.drop_all()
    app_context.pop()


# заполнение базы данных
@pytest.fixture(scope='session')
def add_data_to_db(app):
    add_user_base()

    add_brands_base()

    add_cars_base()

    add_reviews_base()
