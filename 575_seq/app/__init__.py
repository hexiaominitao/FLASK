import os

from flask import Flask, redirect, url_for
from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_login import current_user

from .models import db, User,Role,SeqInfo,RunInfo
from .ext import bcrypt, admin, principal, login_manager
from app.seq_info.admin import CustomView, CustomModeView, CustomFileAdmin


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    db.init_app(app)
    bcrypt.init_app(app)
    admin.init_app(app)
    principal.init_app(app)
    login_manager.init_app(app)
    admin.add_view(CustomView(name='Custom'))
    models = [User,Role,SeqInfo,RunInfo]

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
        return redirect(url_for('bp_seq.index'))

    from .seq_info.seq import bp_seq
    from .seq_info.main import main
    app.register_blueprint(bp_seq)
    app.register_blueprint(main)
    return app
