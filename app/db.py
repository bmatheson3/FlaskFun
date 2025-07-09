## flaskr/db.py
import sqlite3
import click
from flask import current_app, g
    
def get_db():
    ## Check if 'db' is not in 'g'
    if 'db' not in g:
        ## Establish a connection to the database
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        ## Return rows that behave like dicts
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    ## Pop 'db' from 'g' and close the connection if it exists
    db = g.pop('db', None)

    if db is not None:
        db.close()