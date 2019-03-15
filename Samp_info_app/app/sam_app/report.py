import os
from os import path
from flask import render_template, Blueprint, redirect, url_for, abort, request, current_app, flash, send_from_directory

from ..extensions import get_seq_info, file_seq, time_set
from ..models import db, User, RunInfo, SeqInfo, Sample
from ..forms import CheckForm, FormProject, SeqInfoForm, SeqUploadForm

rep_bp = Blueprint('rep_bp', __name__, template_folder=path.join(path.pardir, 'templates', 'rep'), url_prefix="/rep")


@rep_bp.route('/', methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     s_option = request.values.getlist("s_option")
    #     for s in s_option:
    #         print(s)
    df = {
        "pages": RunInfo.query.all()
    }
    # form = FormProject()
    # if form.validate_on_submit():
    #     print()
    if request.method == 'POST':
        print(request.values.getlist('do_delete'))

    return render_template('seq.html', **df)


@rep_bp.route('/runinfo/', methods=['GET', 'POST'])
def runinfo():
    df = {
        "runinfos": RunInfo.query.order_by(RunInfo.start_T.desc()).all()
    }
    # seq1 = SeqInfo.query.filter(SeqInfo.sample_mg == 'MG1916670037').first()
    # print(seq1.sample_info.迈景编号)
    def seq_run(name):
        seq = SeqInfo.query.filter(SeqInfo.run_info_id == name).all()
        return seq
    return render_template('runinfo.html', **df, seq_run=seq_run)


@rep_bp.route('/rep_mut/')
def rep_mut():
    return render_template('rep_mut.html')


@rep_bp.route('/seqinfo/')
def seqinfo():
    return render_template('seqinfo.html')


@rep_bp.route('/muinfo/')
def muinfo():
    return render_template('muinfo.html')


@rep_bp.route('/mufinfo/')
def mufinfo():
    return render_template('mufinfo.html')


@rep_bp.route('/musinfo/')
def musinfo():
    return render_template('musinfo.html')


@rep_bp.route('/repinfo/')
def repinfo():
    return render_template('repinfo.html')


# 文件上传
@rep_bp.route('/upload/add/', methods=['GET', 'POST'])
def upload():
    form = SeqInfoForm()

    if form.validate_on_submit():

        if RunInfo.query.filter(RunInfo.name == form.run.data).first():
            pass
        else:
            run = RunInfo(name=form.run.data, platform=form.platform.data,
                          start_T=form.start.data, end_T=form.end.data)
            db.session.add(run)
            db.session.commit()
    return render_template('run_edit.html', form=form)


@rep_bp.route('/upload/seq_info/', methods=['GET', 'POST'])
def up_seqinfo():
    form = SeqUploadForm()
    path_zip = current_app.config['UPLOADED_FILESEQ_DEST']
    if request.method == 'GET':
        for file in os.listdir(path_zip):
            os.remove(os.path.join(path_zip, file))
    if form.validate_on_submit():
        for filename in request.files.getlist('file'):
            file_seq.save(filename)
        for file in os.listdir(path_zip):
            if file:
                print(file)
                df_seq, title = get_seq_info(os.path.join(path_zip, file))
                for name, df1 in df_seq:
                    df = df1.fillna('')
                    if RunInfo.query.filter(RunInfo.name == name).first():
                        pass
                    else:
                        run = RunInfo(name=name, platform=title,
                                      start_T=time_set(df['上机时间'].unique()[0]),
                                      end_T=time_set(df['结束时间'].unique()[0]))
                        db.session.add(run)
                        db.session.commit()
                    index_seq = df.index
                    run_seq = RunInfo.query.filter(RunInfo.name == name).first()
                    for item in index_seq:
                        if SeqInfo.query.filter(SeqInfo.sample_name == df.loc[item]['迈景编号']).first():
                            pass
                        else:
                            seq = SeqInfo(sample_name=df.loc[item]['迈景编号'])
                            seq.sample_mg = df.loc[item]['申请单号']
                            seq.item = df.loc[item]['检测内容']
                            seq.barcode = df.loc[item]['Barcode编号']
                            seq.note = df.loc[item]['备注']
                            sample = Sample.query.filter(Sample.申请单号 == str(df.loc[item]['申请单号'])).first()
                            print(sample.申请单号)
                            seq.run_info = run_seq
                            seq.sample_info = sample
                            db.session.add(seq)
                            db.session.commit()
            os.remove(os.path.join(path_zip, file))
            return redirect(url_for('rep_bp.runinfo'))
    return render_template('seq_up.html', form=form)


@rep_bp.route('/upload/mut_info/')
def up_mutinfo():
    return 'hello'
