from flask_mail import Message
from .extensions import celery,mail


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def send_mail(self):
    msg = Message('hello',
                  sender='hm@maijinggene.com',
                  recipients=['hmj@maijinggene.com']
    )
    msg.body='hello'
    mail.send(msg)