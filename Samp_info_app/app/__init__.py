import os

from flask import Flask, redirect, url_for
from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_login import current_user
from flask_uploads import configure_uploads, patch_request_class

from .config import DevConfig
from .models import db, User, Post, Tag, Comment, Role, Fastqc, Bamqc, Sample, Report, Mutation, RunInfo, SeqInfo
from .sam_app.admin import CustomView, CustomModeView, CustomFileAdmin
from .extensions import bcrypt, login_manager, principal, admin, cache, file_sample_info, file_fastq_qc, file_bam_qc, \
    mail, celery, file_zip, file_seq


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)
    admin.init_app(app)
    mail.init_app(app)
    celery.init_app(app)

    # cache.init_app(app)

    # 文件上传
    configure_uploads(app, file_sample_info)  # 样本信息表
    configure_uploads(app, file_fastq_qc)  # fast_qc
    configure_uploads(app, file_bam_qc)  # bam_qc
    configure_uploads(app, file_zip)
    configure_uploads(app, file_seq)
    patch_request_class(app)

    admin.add_view(CustomView(name='Custom'))
    models = [User, Post, Tag, Comment, Role, Fastqc, Bamqc, Sample, Report, Mutation, RunInfo, SeqInfo]

    for model in models:
        admin.add_view(
            CustomModeView(model, db.session, category='数据库管理 ')
        )

    admin.add_view(CustomFileAdmin(
        os.path.join(os.path.dirname(__file__), 'static'),
        '/static/', name='静态文件管理'
    ))

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # 设置当前用户身份为login登录对象
        identity.user = current_user

        # 添加UserNeed到identity user对象
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # 每个Role添加到identity user对象，roles是User的多对多关联
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    @app.route('/')
    def index():
        return redirect(url_for('sam_bp.index'))

    from .sam_app.samp import sam_bp
    from .sam_app.main import main_bp
    from .sam_app.report import rep_bp
    app.register_blueprint(sam_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(rep_bp)
    return app
