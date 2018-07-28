import os
import sqlite3
from flask import Flask
from flask import render_template

app = Flask(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'instance', 'hotflask.sqlite')

#the homepage for the application
@app.route('/')
def index():

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT restaurant.name, restaurant.address, city.zipcode, city.name, restaurant.rating, restaurant.price_range FROM restaurant INNER JOIN city on restaurant.zipcode=city.zipcode LIMIT 20;")
    data = cur.fetchall()
            
    return render_template('index.html', data=data)

@app.route('/star_desc')
def star_desc():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT restaurant.name, restaurant.address, city.zipcode, city.name, restaurant.rating, restaurant.price_range FROM restaurant INNER JOIN city on restaurant.zipcode=city.zipcode ORDER BY -restaurant.rating ASC;")
    data = cur.fetchall()
            
    return render_template('index.html', data=data)

