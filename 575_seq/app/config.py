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
    #celery 配置
    CELERY_BROKER_URL = 'amqp://guest@localhost//'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # 邮件服务  腾讯企业邮箱
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


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
    #celery 配置
    CELERY_BROKER_URL = 'amqp://guest@localhost//'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # 邮件服务  腾讯企业邮箱
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
