import csv
import pandas as pd
from pandas import DataFrame

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_admin import Admin
from flask_cache import Cache
from flask_uploads import UploadSet, DOCUMENTS, DATA
from celery import Celery

bcrypt = Bcrypt()
login_manager = LoginManager()
principal = Principal()
admin = Admin()
cache = Cache()

file_sample_info = UploadSet('filesam', DOCUMENTS) #文件上传
file_fastq_qc = UploadSet('filefastq', DATA)
file_bam_qc = UploadSet('filebam', DOCUMENTS)

login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

admin_permission = Permission(RoleNeed('admin'))  # 添加权限 与manage 对应
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(user_id)


# def make_celery(app):
#     celery = Celery(
#         app.import_name, broker=app.config['CELERY_BROKER_URL'],
#         backend=app.config['CELERY_BACKEND']
#     )
#     celery.conf.updata(app.config)
#     TaskBase = celery.Task
#
#     class ContexTask(TaskBase):
#         abstract = True
#
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#
#     celery.Task = ContexTask
#
#     return celery




def excel_rd(path_xl):
    data_sample = pd.read_excel(path_xl, sep='/t', encoding='utf-8')
    df = DataFrame(data_sample)
    return df


def file_to_df(file):
    data_qc = []
    index_qc = []
    with open(file, 'r')as f1:
        f2 = csv.reader(f1, delimiter='\t')
        title = next(f2)
        for row in f2:
            sample_name_list = (row[title.index("#Sample_name")].split('/')[-1]).split('_')
            runname = (row[title.index("#Sample_name")].split('/')[-3])
            sample_name = '{}_{}'.format(sample_name_list[0], sample_name_list[2])
            index_qc.append(sample_name)
            data_qc.append(row[1:])
    df = DataFrame(data_qc, index=index_qc, columns=title[1:], dtype=int)
    df['Reads_p'] = df['Reads_num'] / df['Reads_num'].sum()
    df['Runname'] = runname

    return df, index_qc
