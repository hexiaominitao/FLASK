from flask_script import Manager, Shell, Server
from main import app, db, User,Post,Tag
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_contex():
    return dict(app=app,db=db,User=User,Post=Post,Tag=Tag)


if __name__ == '__main__':
    manager.run()
