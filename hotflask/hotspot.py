import os
from flask import Flask
from flask import render_template

app = Flask(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'instance', 'hotflask.sqlite')

#the homepage for the application
@app.route('/')
def index():
    import sqlite3

    print(DATABASE)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM restaurant LIMIT 20;")
    data = cur.fetchall()
            
    return render_template('index.html', data=data)




