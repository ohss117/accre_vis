'''
Created on Jul 3, 2015

@author: sung
'''
import sqlite3
import os
import json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
from flask.helpers import send_from_directory



# configuration
DATABASE = 'data.db'
DEBUG = True
SECRET_KEY = os.environ.get("FLSK_SECRET_KEY")
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_db():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.enable_load_extension(True)
    connection.load_extension("./fts5")
    return connection
    

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
@app.route('/favicon_ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon-310.png', mimetype='image/vnd.microsoft.icon')


@app.route('/_test')
def test(methods=['GET']):
    
    my_query = g.db.execute('SELECT INSTITUTION_NAME, INSTITUTION_STATE FROM ACCREDITATION_2015_6_V \
                        WHERE INSTITUTION_STATE = "AR" GROUP BY INSTITUTION_NAME, INSTITUTION_STATE')
    
    return json.dumps(my_query.fetchall())


@app.route('/_form')
def form(methods=['GET']):
    
    state = request.args.get('state')
    g.db.row_factory = dict_factory
    my_query = g.db.execute('SELECT INSTITUTION_ID, INSTITUTION_NAME, INSTITUTION_STATE FROM ACCREDITATION_2015_6_V WHERE \
                         INSTITUTION_STATE = ? GROUP BY INSTITUTION_ID, INSTITUTION_NAME, INSTITUTION_STATE limit 10', [state])
    
   
    
    return jsonify(my_result=my_query.fetchall())
    
@app.route('/_search_schools')
def search_schools(methods=['GET']):
    name = request.args.get('term')
    
    name = name.lower() + "*"
    g.db.row_factory = lambda cursor, row: row[0]
    
    query = g.db.execute('SELECT INSTITUTION_NAME, INSTITUTION_ID FROM SCHOOL_NAMES_FTS WHERE SCHOOL_NAMES_FTS MATCH ? ORDER BY RANK LIMIT 10', [name])
   
    
    return jsonify(names = query.fetchall())    
    
@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()