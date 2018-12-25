import os


class Config(object):
    SECRET_KEY = '40f3fea290191b1878144f83f2e3f3ef'


class DevConfig(Config):
    DIALECT = "mysql"
    DRIVER = 'pymysql'
    USERNAME = os.environ.get('SQL_USERNAME')
    PASSWORD = os.environ.get('SQL_PASSWORD')
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = os.environ.get('SQL_DATABASE')
    MY_SQL = 'mysql+pymysql://{}:{}@127.0.0.1:3306/{}?charset=utf8'.format(USERNAME, PASSWORD, DATABASE)
    SQLALCHEMY_DATABASE_URI = MY_SQL
    DEBUG = True


class ProConfig(Config):
    DIALECT = "mysql"
    DRIVER = 'pymysql'
    USERNAME = os.environ.get('SQL_USERNAME')
    PASSWORD = os.environ.get('SQL_PASSWORD')
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = os.environ.get('SQL_DATABASE')
    MY_SQL = 'mysql+pymysql://{}:{}@127.0.0.1:3306/{}?charset=utf8'.format(USERNAME, PASSWORD, DATABASE)
    SQLALCHEMY_DATABASE_URI = MY_SQL
