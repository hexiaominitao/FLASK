import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint, redirect, url_for, abort, request
from flask_login import login_required
from flask_principal import Permission, UserNeed

from ..models import db, Post, Tag, Comment, User, tags
from ..forms import CommentFrom, PostForm, SampleUploadForm, FastqUploadForm, BamUploadForm
from ..extensions import poster_permission, admin_permission, default_permission, file_bam_qc, file_fastq_qc, \
    file_sample_info

sam_bp = Blueprint('sam_bp', __name__, template_folder=path.join(path.pardir, 'templates', 'samp'), url_prefix="/samp")


# template_folder=path.join(path.pardir,'templates','sam_app')
def sidebar_data():
    recent = Post.query.order_by(Post.publish_data.desc()).limit(5).all()
    top_tags = db.session.query(Tag, func.count(tags.c.post_id).label('total')).join(tags).group_by(Tag).order_by(
        'total DESC').limit(5).all()
    return recent, top_tags


@sam_bp.route('/')
def index():
    return render_template('index.html')


@sam_bp.route('/new/', methods=['GET', 'POST'])
@login_required
@default_permission.require(http_exception=403)
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data)
        new_post.text = form.text.data
        new_post.publish_data = datetime.datetime.now()

        db.session.add(new_post)
        db.session.commit()

    return render_template('new.html', form=form)


# @sam_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# @poster_permission.require(http_exception=403)
# def edit_post(id):
#     post = Post.query.get_or_404(id)
#     permission = Permission(UserNeed(post.user_id))
#     if permission.can() or admin_permission.can():
#
#         form = PostForm()
#
#         if form.validate_on_submit():
#             post.title = form.title.data
#             post.text = form.text.data
#             post.publish_data = datetime.datetime.now()
#
#             db.session.add(post)
#             db.session.commit()
#
#             return redirect(url_for('.post', post_id=post.id))
#
#         form.text.data = post.text
#
#         return render_template('edit.html', post=post, form=form)
#     abort(403)


@sam_bp.route('/fileupload/', methods=['GET', 'POST'])
def upload_sam():
    filename = None
    sam_form = SampleUploadForm()
    fastq_form = FastqUploadForm()
    bam_form = BamUploadForm()
    if sam_form.validate_on_submit():
        print('hah')
        for filename in request.files.getlist('file'):
            file_sample_info.save(filename)

    if fastq_form.validate_on_submit():
        for filename in request.files.getlist('file'):
            file_fastq_qc.save(filename)

    if bam_form.validate_on_submit():
        for filename in request.files.getlist('file'):
            file_bam_qc.save(filename)
    return render_template('upload.html', sam_form=sam_form, fastq_form=fastq_form, bam_form=bam_form)


@sam_bp.route('/sampleinfo/', methods=['GET', 'POST'])
def sample_info():
    return render_template('sampleinfo.html')


@sam_bp.route('/fastqc/', methods=['GET', 'POST'])
def fastq_qc():
    return render_template('fastqc.html')


@sam_bp.route('/bamqc/', methods=['GET', 'POST'])
def bam_qc():
    return render_template('bamqc.html')
