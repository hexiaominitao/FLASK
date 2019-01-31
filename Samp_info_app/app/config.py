import os
import tempfile


class Config(object):
    # cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32 获取随机字符
    SECRET_KEY = '40f3fea290191b1878144f83f2e3f3ef'
    RECAPTCHA_PUBLIC_KEY = '6LeKgIEUAAAAAFxgWOvLHrWt89IWO3v0qFlzQfaJ'
    RECAPTCHA_PRIVATE_KEY = '6LeKgIEUAAAAAICNkNTkHXEhNttIL3ncm-a7cJFB'
    UPLOADED_FILESAM_DEST = 'app/static/up_file'
    UPLOADED_FILEFASTQ_DEST = 'app/static/up_file'
    UPLOADED_FILEBAM_DEST = 'app/static/up_file'
    UPLOADED_FILEZIP_DEST = 'app/static/zip'
    VCF_FILE = 'app/static/vcf_file'
    REPORT = 'app/static/report'


class ProdConfig(Config):
    # CACHE_TYPE = 'simple'
    DIALECT = "mysql"
    DRIVER = 'pymysql'
    USERNAME = os.environ.get('SQL_USERNAME')
    PASSWORD = os.environ.get('SQL_PASSWORD')
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = os.environ.get('SQL_DATABASE')
    MY_SQL = 'mysql+pymysql://{}:{}@127.0.0.1:3306/{}?charset=utf8'.format(USERNAME, PASSWORD, DATABASE)
    SQLALCHEMY_DATABASE_URI = MY_SQL
    CACHE_TYPE = 'null'
    UPLOADED_FILESAM_DEST = 'app/static/up_file'
    UPLOADED_FILEFASTQ_DEST = 'app/static/up_file'
    UPLOADED_FILEBAM_DEST = 'app/static/up_file'

    # celery 配置
    CELERY_BROKER_URL = 'amqp://guest@localhost//'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # 邮件服务  腾讯企业邮箱
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class DevConfig(Config):
    DEBUG = True
    DIALECT = "mysql"
    DRIVER = 'pymysql'
    USERNAME = os.environ.get('SQL_USERNAME')
    PASSWORD = os.environ.get('SQL_PASSWORD')
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = os.environ.get('SQL_DATABASE')
    MY_SQL = 'mysql+pymysql://{}:{}@127.0.0.1:3306/{}?charset=utf8'.format(USERNAME, PASSWORD, DATABASE)
    SQLALCHEMY_DATABASE_URI = MY_SQL
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'null'
    #文件上传路径

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


class TestConfig(Config):
    db_file = tempfile.NamedTemporaryFile()
    DEBUG = True
    DEBUG_TB_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file.name
    CACHE_TYPE = 'null'
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')