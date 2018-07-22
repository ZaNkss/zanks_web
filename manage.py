import os

# from flask_sqlalchemy import SQLAlchemy

from app import create_app
from flask_script import Manager



app = create_app('default')
# 创建数据库实例对象

manager = Manager(app)
#migrate = Migrate(app, db)


# def make_shell_context():
#     return dict(app=app, db=db, User=User, Role=Role)
# manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':

    app.run()