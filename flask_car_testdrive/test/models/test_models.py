import pytest

from app import db
from app.models import Users
from app.user.email import send_email
from config import Config


@pytest.mark.usefixtures('db')
class TestRegister:

    def test_register(self):
        user = Users(name='danila')
        db.session.add(user)
        db.session.commit()

        user = Users.query.all()
        assert len(user) == 1
        assert user[0].name == 'danila'

    # @pytest.mark.parametrize('')
    # def test_some(self):
    #     pass


def test_email():
    subject = 'Your testdrive on: '
    body = 'Hello, your testdrive date: '
    attachments = 'static/profile_image/default.jpg'
    send_email(subject, Config.MAIL_USERNAME, [Config.MAIL_USERNAME], body, attachments)
