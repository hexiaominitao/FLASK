import pyinotify, os

from flask_mail import Message
from .extensions import celery, mail, file_to_df
from .models import Fastqc, db


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
    msg.body = 'hello'
    mail.send(msg)


class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        name = event.pathname
        print(name)
        if name.endswith(".csv"):
            file = os.path.join('/home/hemin/Desktop/inotifydir', name)
            df, index_qc = file_to_df(file)

            for item in index_qc:
                fastq_info = Fastqc(迈景编号=str(df.loc[item]['Runname']),
                                    样本编号=item,
                                    Reads数=int(df.loc[item]['Reads_num']),
                                    Reads占比=float(df.loc[item]['Reads_p']),
                                    Q20=float(df.loc[item]['Q20']),
                                    Q30=float(df.loc[item]['Q30']),
                                    GC比例=float(df.loc[item]['GC_rate']),
                                    N比例=int(df.loc[item]['N_couunt']))
                # Base数 = int(df.loc[item]['Base_num']),
                if Fastqc.query.filter(Fastqc.样本编号 == item).first():
                    pass
                else:
                    db.session.add(fastq_info)
                    db.session.commit()
            os.remove(file)


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def whatch_dir(self):
    wm = pyinotify.WatchManager()
    wm.add_watch('/home/hemin/Desktop/inotifydir', pyinotify.ALL_EVENTS, rec=True)
    eh = MyEventHandler()
    notifiter = pyinotify.Notifier(wm, eh)
    notifiter.loop()