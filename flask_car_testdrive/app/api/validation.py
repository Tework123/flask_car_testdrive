import re
from app.api.errors import ApiUserError
# from app.models import Users


class UserFieldValidation:
    def __init__(self, data):
        self.data = data

    def email_validation(self):
        if Users.query.filter_by(email=self.data).first():
            raise ApiUserError('email already use', 400)
        if '@' not in self.data or '.' not in self.data:
            raise ApiUserError('email incorrect', 400)

    def password_validation(self):
        if not 4 < len(self.data) < 25 or not any(map(str.isdigit, self.data)):
            raise ApiUserError('password length: 5-24, number must be', 400)

    def phone_validation(self):
        if not bool(re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
                             self.data)):
            raise ApiUserError('incorrect phone number', 400)

    def name_validation(self):
        if not 3 < len(self.data) < 25:
            raise ApiUserError('name length: 4-24', 400)
