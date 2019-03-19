import os
from os import path
from flask import render_template, Blueprint, redirect, url_for, abort, request, current_app, flash, send_from_directory
from flask_login import current_user
from sqlalchemy import func, or_, and_

from ..extensions import get_seq_info, file_seq, time_set, file_zip, unzip_file, ir10087, archive_file
from ..models import db, User, RunInfo, SeqInfo, Sample, Report, Mutation
from ..forms import CheckForm, FormProject, SeqInfoForm, SeqUploadForm, MuUpForm

rep_bp = Blueprint('rep_bp', __name__, template_folder=path.join(path.pardir, 'templates', 'rep'), url_prefix="/rep")


def status_name(name):
    status = Report.query.filter(Report.sam_id == name).first()
    if status:
        return '{} {}'.format(status.user.username, status.status)
    else:
        return '上机'


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


@rep_bp.route('/runinfo/', methods=['GET', 'POST'])  # 上机信息
def runinfo():
    df = {
        "runinfos": RunInfo.query.order_by(RunInfo.start_T.desc()).all()
    }

    # seq1 = SeqInfo.query.filter(SeqInfo.sample_mg == 'MG1916670037').first()
    # print(seq1.sample_info.迈景编号)
    def seq_run(name):
        seq = SeqInfo.query.filter(SeqInfo.run_info_id == name).all()
        return seq

    if 'report' in request.form:
        report_mg = request.form.getlist('check')
        for name in report_mg:
            if Report.query.filter(Report.sam_id == name).first():
                pass
            else:
                sample = Sample.query.filter(Sample.申请单号 == name).first()
                item = SeqInfo.query.filter(SeqInfo.sample_mg == name).first()
                report = Report(sam_id=name)
                report.report = sample
                report.sam = sample.迈景编号
                report.name = '{}_{}基因检测报告'.format(name, item.item)
                report.status = '制作中'
                report.user = current_user
                db.session.add(report)
                db.session.commit()
        return redirect(url_for('.seqinfo'))

    return render_template('runinfo.html', **df, seq_run=seq_run, status_name=status_name)


@rep_bp.route('/rep_mut/<sample_mg>', methods=['GET', 'POST'])  # 突变初审
def rep_mut(sample_mg):
    df = {
        'report': Report.query.filter(Report.sam_id == sample_mg).first()
    }
    if 'pass' in request.form:
        mut_id = request.form.getlist('check')
        mut_note = request.form.getlist('note')
        for id, note in zip(mut_id, mut_note):
            print(id, note)
            Mutation.query.filter(Mutation.id == id).update({
                '状态': '初审通过',
                '备注': note
            })
            db.session.commit()
        return redirect(url_for('.rep_mut', sample_mg=sample_mg))
    if 'npass' in request.form:
        mut_id = request.form.getlist('check')
        mut_note = [x for x in request.form.getlist('note') if x != '']
        print(mut_id)
        print(mut_note)
        for id, note in zip(mut_id, mut_note):
            print(id, note)
            Mutation.query.filter(Mutation.id == id).update({
                '状态': '初审未通过',
                '备注': note
            })
            db.session.commit()
        return redirect(url_for('.rep_mut', sample_mg=sample_mg))

    return render_template('rep_mut.html', **df, sample_mg=sample_mg)


@rep_bp.route('/seqinfo/', methods=['GET', 'POST'])  # 报告制作
def seqinfo():
    user = current_user
    df = {
        'report': Report.query.filter(and_(Report.status == '制作中', Report.user_id == user.id)).all()
    }

    def mutation_conut(sam_id):
        rep = Report.query.filter(Report.sam_id == sam_id).first()
        mutation = Mutation.query.filter(Mutation.mutation == rep).all()
        return len(list(mutation))

    if 'cancel' in request.form:
        report_mg = request.form.getlist('check')
        for name in report_mg:
            seq = Report.query.filter(Report.sam_id == name).first()
            mutation = Mutation.query.filter(Mutation.mutation == seq).all()
            if mutation:
                for mut in mutation:
                    db.session.delete(mut)
            db.session.delete(seq)

        db.session.commit()
        return redirect(url_for('.seqinfo'))

    if 'check_f' in request.form:
        report_mg = request.form.getlist('check')
        for name in report_mg:
            rep = Report.query.filter(Report.sam_id == name).first()
            mutation = Mutation.query.filter(Mutation.mutation == rep).all()
            if mutation:
                Report.query.filter(Report.sam_id == name).update({'status': '等待审核'})
                db.session.commit()
        return redirect(url_for('.seqinfo'))

    return render_template('seqinfo.html', **df, status_name=status_name, mutation_conut=mutation_conut)


@rep_bp.route('/muinfo/<sample_mg>', methods=['GET', 'POST'])  # 突变二审
def muinfo(sample_mg):
    df = {
        'report': Report.query.filter(Report.sam_id == sample_mg).first()
    }
    if 'pass' in request.form:
        mut_id = request.form.getlist('check')
        mut_note = request.form.getlist('note')
        for id, note in zip(mut_id, mut_note):
            print(id, note)
            Mutation.query.filter(Mutation.id == id).update({
                '状态': '审核通过',
                '备注': note
            })
            db.session.commit()
        return redirect(url_for('.muinfo', sample_mg=sample_mg))
    if 'npass' in request.form:
        mut_id = request.form.getlist('check')
        mut_note = [x for x in request.form.getlist('note') if x != '']
        print(mut_id)
        print(mut_note)
        for id, note in zip(mut_id, mut_note):
            print(id, note)
            Mutation.query.filter(Mutation.id == id).update({
                '状态': '审核未通过',
                '备注': note
            })
            db.session.commit()
        return redirect(url_for('.muinfo', sample_mg=sample_mg))
    return render_template('muinfo.html', **df, sample_mg=sample_mg)


@rep_bp.route('/mufinfo/', methods=['GET', 'POST'])  # 结果二审
def mufinfo():
    df = {
        'report': Report.query.filter(Report.status == '等待审核').all()
    }

    def mutation_conut(sam_id):
        rep = Report.query.filter(Report.sam_id == sam_id).first()
        mutation_all = Mutation.query.filter(Mutation.mutation == rep).all()

        return len(list(mutation_all))

    if 'cancel' in request.form:
        report_mg = request.form.getlist('check')
        for name in report_mg:
            Report.query.filter(Report.sam_id == name).update({'status': '制作中'})

        db.session.commit()
        return redirect(url_for('.mufinfo'))

    if 'check_f' in request.form:
        report_mg = request.form.getlist('check')
        for name in report_mg:
            Report.query.filter(Report.sam_id == name).update({'status': '审核通过'})
        db.session.commit()
        return redirect(url_for('.mufinfo'))
    return render_template('mufinfo.html', **df, status_name=status_name, mutation_conut=mutation_conut)


@rep_bp.route('/musinfo/', methods=['GET', 'POST'])  # 生成报告
def musinfo():
    df = {
        'report': Report.query.filter(Report.status == '审核通过').all()
    }

    def mutation_conut(sam_id):
        rep = Report.query.filter(Report.sam_id == sam_id).first()
        mutation_all = Mutation.query.filter(Mutation.mutation == rep).all()
        return len(list(mutation_all))

    if 'cancel' in request.form:
        report_mg = request.form.getlist('check')
        for name in report_mg:
            Report.query.filter(Report.sam_id == name).update({'status': '等待审核'})

        db.session.commit()
        return redirect(url_for('.musinfo'))

    if 'check_f' in request.form:
        report_mg = request.form.getlist('check')
        for name in report_mg:
            Report.query.filter(Report.sam_id == name).update({'status': '审核完成'})
        db.session.commit()
        return redirect(url_for('.musinfo'))
    return render_template('musinfo.html', **df, status_name=status_name, mutation_conut=mutation_conut)


@rep_bp.route('/musinfo/<sample_mg>/', methods=['GET', 'POST'])  # 生成报告
def musinfo_mg(sample_mg):
    df = {
        'report': Report.query.filter(Report.sam_id == sample_mg).first()
    }
    return render_template('mutation_f.html', **df, sample_mg=sample_mg)


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


@rep_bp.route('/upload/<sample_mg>/', methods=['GET', 'POST'])
def up_mutinfo(sample_mg):
    form = MuUpForm()
    status = Report.query.filter(Report.sam_id == sample_mg).first()
    path_file = current_app.config['UPLOADED_FILEZIP_DEST']
    path_report = current_app.config['REPORT']
    path_vcf = current_app.config['VCF_FILE']
    if form.validate_on_submit():
        for filename in request.files.getlist('file'):
            file_zip.save(filename)
        for file in os.listdir(path_file):
            if status.sam in file:
                vcf_file = unzip_file(path_report, path_file, path_vcf, file, sample_mg)
                mutation = ir10087(sample_mg, vcf_file, path_report)
                title_mu = mutation[0]
                for row in mutation[1:]:
                    def mutat_ion(item):
                        return row[title_mu.index(item)]

                    if Mutation.query.filter(and_(Mutation.突变全称 == mutat_ion('突变全称'),
                                                  Mutation.mutation == status)).first():
                        pass
                    else:
                        mutations = Mutation(基因=mutat_ion('基因'),
                                             突变类型=mutat_ion('突变类型'),
                                             突变名称=mutat_ion('突变名称'),
                                             突变全称=mutat_ion('突变全称'),
                                             突变频率=mutat_ion('突变频率'),
                                             覆盖度=mutat_ion('覆盖度'),
                                             位置=mutat_ion('位置'), 状态='未审核',
                                             mutation=status
                                             )
                        db.session.add(mutations)
                    db.session.commit()
                    archive_file(path_report, sample_mg)
        return redirect(url_for('rep_bp.seqinfo'))
    return render_template('mutation_up.html', form=form, status=status)
