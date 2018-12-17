import os


from flask_script import Manager, Shell, Server
from app.models import db, User,Post,Tag,Comment
from app import create_app
from flask_migrate import Migrate, MigrateCommand


# env = os.environ.get('SAM_APP_ENV','dev')
# app = create_app('sam_app.config.%sConfig',env.capitalize())
app =create_app()

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_contex():
    return dict(app=app,db=db,User=User,Post=Post,Tag=Tag,Comment=Comment)


if __name__ == '__main__':
    manager.run()
