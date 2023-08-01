from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import check_password_hash

from app.api.errors import error_response
from app.models import Users

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(email, password):
    user = Users.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    else:
        return None


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return Users.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)
