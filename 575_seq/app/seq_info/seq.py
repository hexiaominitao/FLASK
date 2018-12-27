from os import path
from sqlalchemy import func, or_
from flask import render_template, Blueprint, redirect, url_for, abort, request, current_app, flash
from flask_login import login_required, current_user

from ..models import db, SeqInfo, RunInfo
from ..forms import SeqForm, RunForm
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
            run.count = form.count.data
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
            'count': form.count.data,
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
    run = RunInfo.query.filter(RunInfo.name == runname).first()

    df = {
        'status': SeqInfo.query.filter(SeqInfo.run_info_id == run.id).all()
    }

    if form.validate_on_submit():
        if SeqInfo.query.filter(SeqInfo.sample == form.sample.data).first():
            pass
        else:
            seq = SeqInfo(sample=form.sample.data)
            seq.item = form.item.data
            seq.index = form.index.data
            seq.note = form.note.data

            seq.user = current_user
            seq.run_info = run

            db.session.add(seq)
            db.session.commit()
        return redirect(url_for('.seq_info', runname=runname))

    return render_template('seqinfo.html', form=form, **df)


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
            'note' : form.note.data
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


