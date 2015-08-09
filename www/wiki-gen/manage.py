from flask.ext.script import Manager
from wiki_gen import app, init_all_db

manager = Manager(app)


@manager.command
def initdb():
    '''Create all database tables'''
    init_all_db()


if __name__ == '__main__':
    manager.run()
