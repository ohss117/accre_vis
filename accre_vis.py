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
SECRET_KEY = 'MIIEpAIBAAKCAQEAz1dUJmeVg4yF9BoxHB+UTyXy6mabXYrDmAjja5wXeh9G3+8V'
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
    
    
    
@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()