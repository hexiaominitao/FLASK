import os

class Config(object):
    # cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32 获取随机字符
    SECRET_KEY = '40f3fea290191b1878144f83f2e3f3ef'
    RECAPTCHA_PUBLIC_KEY = '6LeKgIEUAAAAAFxgWOvLHrWt89IWO3v0qFlzQfaJ'
    RECAPTCHA_PRIVATE_KEY = '6LeKgIEUAAAAAICNkNTkHXEhNttIL3ncm-a7cJFB'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    DIALECT = "mysql"
    DRIVER = 'pymysql'
    USERNAME = os.environ.get('SQL_USERNAME')
    PASSWORD = os.environ.get('SQL_PASSWORD')
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = os.environ.get('SQL_DATABASE')
    MY_SQL = 'mysql+pymysql://{}:{}@127.0.0.1:3306/{}?charset=utf8'.format(USERNAME,PASSWORD,DATABASE)
    SQLALCHEMY_DATABASE_URI = MY_SQL