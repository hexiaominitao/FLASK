import os

class Config(object):
    pass

class ProdConfig(object):
    pass

class DevConfig(object):
    DEBUG = True
    DIALECT = "mysql"
    DRIVER = 'pymysql'
    USERNAME = os.environ.get('SQL_USERNAME')
    PASSWORD = os.environ.get('SQL_PASSWORD')
    HOST = '127.0.0.1'
    PORT = '3306'
    DATEBASE = os.environ.get('SQL_DATEBASE')
    MY_SQL = 'mysql+pymysql://{}:{}@127.0.0.1:3306/{}?charset=utf8'.format(USERNAME,PASSWORD,DATEBASE)
    SQLALCHEMY_DATABASE_URI = MY_SQL