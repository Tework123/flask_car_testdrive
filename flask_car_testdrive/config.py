import os.path
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    # MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')
    ADMIN_LOGIN = os.environ.get('ADMIN_LOGIN')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    RABBIT_USER = os.environ.get('RABBIT_USER')
    RABBIT_PASSWORD = os.environ.get('RABBIT_PASSWORD')


class DevelopmentConfig(Config):
    name = 'DevelopmentConfig'
    basepath = os.path.abspath("") + '/'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES')
    REDIS_URL = os.environ.get('REDIS_URL_LOCAL')
    RABBIT_HOST = os.environ.get('RABBIT_HOST_local')


class TestingConfig(Config):
    name = 'TestingConfig'
    basepath = os.path.abspath("") + '/'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_TEST')
    REDIS_URL = os.environ.get('REDIS_URL_LOCAL')
    RABBIT_HOST = os.environ.get('RABBIT_HOST_local')


class ProductionConfig(Config):
    name = 'ProductionConfig'
    basepath = os.path.abspath('') + '/flask_car_testdrive/'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_server')
    REDIS_URL = os.environ.get('REDIS_URL_server')
    RABBIT_HOST = os.environ.get('RABBIT_HOST_server')
