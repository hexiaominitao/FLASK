from flask import Flask, redirect, url_for
from flask_principal import identity_loaded, UserNeed, RoleNeed

from .config import DevConfig
from .models import db
from .sam_app.samp import sam_bp
from .sam_app.main import main_bp
from .extensions import bcrypt, login_manager, principal


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(curren_user,identity):
        identity.user = curren_user

        if hasattr(curren_user,'id'):
            identity.provides.add(UserNeed(curren_user.id))

        if hasattr(curren_user,'roles'):
            for role in curren_user.roles:
                identity.provides.add(RoleNeed(role.name))

    @app.route('/')
    def index():
        return redirect(url_for('sam_bp.index'))

    app.register_blueprint(sam_bp)
    app.register_blueprint(main_bp)
    return app
