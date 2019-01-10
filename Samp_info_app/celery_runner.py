import os
from app import create_app
from celery import Celery
from app.tasks import send_mail,whatch_dir


def make_celery(app):
    celery = Celery(
        app.import_name, broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContexTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContexTask

    return celery


flask_app = create_app('app.config.DevConfig')

celery = make_celery(flask_app)
