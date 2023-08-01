import os.path
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ADMINS = os.environ.get('ADMINS')
    ADMIN_LOGIN = os.environ.get('ADMIN_LOGIN')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

    basepath = os.path.abspath("") + '/'


class DevelopmentConfig(Config):
    name = 'DevelopmentConfig'
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES')


class TestingConfig(Config):
    name = 'TestingConfig'
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_TEST')


class ProductionConfig(Config):
    name = 'ProductionConfig'
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_PROD')
