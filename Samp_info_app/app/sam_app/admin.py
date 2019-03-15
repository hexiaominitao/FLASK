from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import login_required, current_user
from ..extensions import admin_permission


class CustomModeView(ModelView):
    # pass
    # can_create = False
    def is_accessible(self):
        return current_user.is_authenticated and admin_permission


class CustomFileAdmin(FileAdmin):
    # pass
    def is_accessible(self):
        return current_user.is_authenticated and admin_permission


class CustomView(BaseView):
    @expose('/')
    @login_required
    @admin_permission.require(http_exception=403)
    def index(self):
        return self.render('admin/custom.html')

    @expose('second_page')
    @login_required
    @admin_permission.require(http_exception=403)
    def second_page(self):
        return self.render('admin/scend_page.html')
