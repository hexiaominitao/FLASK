from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_admin import Admin
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_celery import Celery

bcrypt = Bcrypt()
login_manager = LoginManager()
principal = Principal()
admin = Admin()
ckeditor = CKEditor()
mail = Mail()
celery = Celery()



login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

admin_permission = Permission(RoleNeed('admin'))  # 添加权限 与manage 对应
seq_permission = Permission(RoleNeed('seq'))
default_permission = Permission(RoleNeed('default'))


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(user_id)

