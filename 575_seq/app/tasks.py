from flask_mail import Message
from .ext import celery, mail


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def send_mail(self, object, sen, to, body, html):
    msg = Message(object,
                  sender=sen,
                  recipients=to
                  )
    msg.body = body
    msg.html = html
    mail.send(msg)
