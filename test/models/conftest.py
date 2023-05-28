import pytest
from app import db as _db


@pytest.fixture(scope='function', autouse=True)
def db(app):
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()
