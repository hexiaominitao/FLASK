import os

from flask_script import Manager, Shell, Server
from flask_script.commands import ShowUrls, Clean
from app import create_app
from flask_migrate import Migrate, MigrateCommand

from app.models import db, User, Post, Tag, Comment, Role
from app.config import DevConfig

# env = os.environ.get('SAM_APP_ENV','dev')
# app = create_app('sam_app.config.%sConfig',env.capitalize())
app = create_app(DevConfig)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)
manager.add_command('show_url', ShowUrls())
manager.add_command('clean', Clean())


@manager.shell
def make_shell_contex():
    return dict(app=app, db=db, User=User, Post=Post, Tag=Tag, Comment=Comment, Role=Role)


# @manager.shell
# def set_up():
#     db.create_all()
#
#     admin_role = Role(name='admin')
#     admin_role.description = 'admin'
#     db.session.add(admin_role)
#
#     default_role = Role(name='default')
#     default_role.description = 'default'
#     db.session.add(default_role)
#
#     # default_role = Role(name='default') #添加权限 联系 extensions
#     # default_role.description = 'default'
#     # db.session.add(default_role)
#
    # admin = User(username='admin')
    # admin.set_password("hm714012636")
    # admin.roles.append(admin_role)
    # admin.roles.append(default_role)
    # db.session.add(admin)
    #
    # db.session.commit()


if __name__ == '__main__':
    manager.run()
