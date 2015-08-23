import os
import sqlite3
from flask import Flask, request, render_template, g, url_for

from markov_generator import MarkovGenerator


app = Flask(__name__, static_url_path='')
app.config.from_object('config')


### Database connections
def connect_seeds_db():
    '''Connect to the seeds database'''
    if not hasattr(g, 'db_seeds'):
        g.db_seeds = sqlite3.connect(app.config['DATABASE_SEEDS'])
    return g.db_seeds

def connect_grams_db():
    '''Connect to the grams database'''
    if not hasattr(g, 'db_grams'):
        g.db_grams= sqlite3.connect(app.config['DATABASE_GRAMS'])
    return g.db_grams


### Request hooks
@app.teardown_request
def close_dbs(exception):
    '''Close database connections'''
    for db_key in ['db_seeds', 'db_grams']:
        db = getattr(g, db_key, None) 
        if db is not None:
            db.close()


### Routes
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/gen')
def generate():
    raw_seed = request.args.get('seed')
    if raw_seed is None:
        return 'No seed provided'
    return raw_seed


### Exception handlers
@app.errorhandler(404)
def not_found(exception):
    return 'Page not found', 404

@app.errorhandler(500)
def server_error(exception):
    return 'Server error', 500
