import os
import sqlite3
from flask import Flask, request, render_template, g


app = Flask(__name__)
app.config.from_object('config')


### Database handling/utilities
def connect_seeds_db():
    '''Connect to the seeds database'''
    return sqlite3.connect(app.config['DATABASE_SEEDS'])

def connect_grams_db():
    '''Connect to the grams database'''
    return sqlite3.connect(app.config['DATABASE_GRAMS'])

def init_seeds_db():
    '''Initialize the seeds logging database'''
    if os.path.isfile(app.config['DATABASE_SEEDS']):
        raise Exception('{} already exists'.format(app.config['DATABASE_SEEDS']))
        return
    db = connect_seeds_db()
    with open('schemas/seeds.sql') as f:
        db.cursor().executescript(f.read())
    db.close()

def init_all_db():
    '''Initialize all databases'''
    init_seeds_db()


### Request hooks
@app.before_request
def before_request():
    pass

@app.teardown_request
def teardown_request(exception):
    '''Close database connections'''
    for db_key in ['db_seeds', 'db_grams']:
        db = getattr(g, db_key, None) 
        if db is not None:
            db.close()


### Routes
@app.route('/')
def home():
    return 'Hello!' 

@app.route('/gen')
def generate():
    tokens = request.args.get('seed-tokens')
    return tokens
