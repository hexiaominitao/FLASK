from os import path
from sqlalchemy import func, or_
from flask import render_template, Blueprint, redirect, url_for, abort, request, current_app, flash
from flask_login import login_required, current_user

from ..models import db, SeqInfo, RunInfo, SeqIndex
from ..forms import SeqForm, RunForm, AllSeqForm, IndexForm,PlatForm
from ..ext import default_permission, seq_permission

bp_seq = Blueprint(
    'bp_seq', __name__, template_folder=path.join(path.pardir, 'templates', 'seq'), url_prefix="/seq/")


@bp_seq.errorhandler(403)
def permission_denied(error):
    return render_template('permission_denied.html'), 403


@bp_seq.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@bp_seq.route('/', methods=['POST', 'GET'])
def index():
    df = {
        'status': RunInfo.query.all()
    }
    return render_template('index.html', **df)


@bp_seq.route('/runinfo/', methods=['POST', 'GET'])
@login_required
@default_permission.require(http_exception=403)
@seq_permission.require(http_exception=403)
def run_info():
    form = RunForm()
    if form.validate_on_submit():
        if RunInfo.query.filter(RunInfo.name == form.runname.data).first():
            pass
        else:
            run = RunInfo(name=form.runname.data)
            run.paltform = form.paltform.data
            run.start_T = form.start.data
            run.end_T = form.end.data

            db.session.add(run)
            db.session.commit()
        return redirect(url_for('.index'))

    return render_template('runinfo.html', form=form)


@bp_seq.route('/runinfo/edit_run/<runname>', methods=['POST', 'GET'])
@login_required
@default_permission.require(http_exception=403)
@seq_permission.require(http_exception=403)
def edit_run(runname):
    form = RunForm()

    status = RunInfo.query.filter(RunInfo.name == runname).first()

    if form.validate_on_submit():
        RunInfo.query.filter(RunInfo.name == runname).update({
            'name': form.runname.data,
            'paltform': form.paltform.data,
            'start_T': form.start.data,
            'end_T': form.end.data
        })
        db.session.commit()
        return redirect(url_for('.index'))

    return render_template('edit-run.html', form=form, status=status)


@bp_seq.route('/runinfo/del_run/<runname>', methods=['POST', 'GET'])
@login_required
@default_permission.require(http_exception=403)
@seq_permission.require(http_exception=403)
def del_run(runname):
    status = RunInfo.query.filter(RunInfo.name == runname).first()
    sample = status.seq_info
    for sam in sample:
        db.session.delete(sam)
    db.session.delete(status)
    db.session.commit()
    return redirect(url_for('.index'))


@bp_seq.route('/runinfo/<runname>', methods=['POST', 'GET'])
@login_required
@default_permission.require(http_exception=403)
@seq_permission.require(http_exception=403)
def seq_info(runname):
    form = SeqForm()
    all_form = AllSeqForm()
    run = RunInfo.query.filter(RunInfo.name == runname).first()
    df = {
        'status': SeqInfo.query.filter(SeqInfo.run_info_id == run.id).all()
    }
    paltform = run.paltform

    index_dic = SeqIndex.query.all()
    index_d = {}
    for index_i in index_dic:
        index_d[index_i.name] = index_i.index

    def split_index(index_data):
        tem_index = index_data.split('+')
        if len(tem_index) == 1:
            return index_d.get('{}_{}'.format(paltform, tem_index[0])), ''
        return index_d.get('{}_{}'.format(paltform, tem_index[0])), index_d.get('{}_{}'.format(paltform, tem_index[-1]))

    if form.validate_on_submit():
        if SeqInfo.query.filter(SeqInfo.sample == form.sample.data).first():
            pass
        else:
            seq = SeqInfo(sample=form.sample.data)
            seq.item = form.item.data
            index_data = form.index.data
            seq.index, seq.index_p5 = split_index(index_data)
            seq.note = form.note.data

            seq.user = current_user
            seq.run_info = run

            db.session.add(seq)
            db.session.commit()
        return redirect(url_for('.seq_info', runname=runname))
    if all_form.validate_on_submit():
        a = all_form.seqinfo.data
        b = a.strip().split('\n')
        for c in b:
            d = c.split('\t')
            if SeqInfo.query.filter(SeqInfo.sample == d[0]).first():
                pass
            else:
                seq = SeqInfo(sample=d[0])
                seq.item = d[1]
                index_data = d[2]
                seq.index, seq.index_p5 = split_index(index_data)
                seq.note = d[3]

                seq.user = current_user
                seq.run_info = run

                db.session.add(seq)
        db.session.commit()
        return redirect(url_for('.seq_info', runname=runname))

    return render_template('seqinfo.html', form=form, all_form=all_form, run=run, **df)


@bp_seq.route('/runinfo/edit/<samlpe>', methods=['POST', 'GET'])
@login_required
@default_permission.require(http_exception=403)
@seq_permission.require(http_exception=403)
def edit_seq(samlpe):
    form = SeqForm()

    status = SeqInfo.query.filter(SeqInfo.sample == samlpe).first()
    runname = status.run_info.name
    if form.validate_on_submit():
        SeqInfo.query.filter(SeqInfo.sample == samlpe).update({
            'sample': form.sample.data,
            'item': form.item.data,
            'index': form.index.data,
            'index_p5': form.index_p5.data,
            'note': form.note.data
        })
        db.session.commit()
        return redirect(url_for('.seq_info', runname=runname))

    return render_template('edit.html', form=form, status=status)


@bp_seq.route('/runinfo/del/<samlpe>', methods=['POST', 'GET'])
@login_required
@default_permission.require(http_exception=403)
@seq_permission.require(http_exception=403)
def del_seq(samlpe):
    status = SeqInfo.query.filter(SeqInfo.sample == samlpe).first()
    runname = status.run_info.name
    db.session.delete(status)
    db.session.commit()
    return redirect(url_for('.seq_info', runname=runname))


@bp_seq.route('/runinfo/up_index', methods=['POST', 'GET'])
@login_required
@default_permission.require(http_exception=403)
@seq_permission.require(http_exception=403)
def up_index():
    form = IndexForm()
    if form.validate_on_submit():
        a = form.indexinfo.data
        b = a.strip().split('\n')
        for c in b:
            d = c.split('\t')
            if SeqIndex.query.filter(SeqIndex.name == d[0]).first():
                pass
            else:
                seq_index = SeqIndex(name=d[0])
                seq_index.index = d[1]
                db.session.add(seq_index)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('up_index.html', form=form)


@bp_seq.route('/select/', methods=['POST', 'GET'])
def select_t():
    form = PlatForm()
    return render_template('test.html', form=form)