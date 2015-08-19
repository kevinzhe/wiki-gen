import os
from flask.ext.script import Manager
from wiki_gen import app, connect_seeds_db


def init_seeds_db():
    '''Initialize the seeds logging database'''
    if os.path.isfile(app.config['DATABASE_SEEDS']):
        raise NameError('{} already exists'.format(app.config['DATABASE_SEEDS']))
        return 1
    db = connect_seeds_db()
    with open('schemas/seeds.sql') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()



manager = Manager(app)

@manager.command
def initdb():
    '''Create all database tables'''
    try:
        init_seeds_db()
    except NameError as e:
        print e.message
        return 1
    except:
        print 'There was an error creating the database'
        return 1
    print 'Database created'
    return 0

@manager.command
def runglobalserver():
    '''Run the server on 0.0.0.0'''
    app.run(host='0.0.0.0')

@manager.command
def runservernodebug():
    '''Run the server on localhost without debug'''
    app.run(debug=False)

if __name__ == '__main__':
    manager.run()
