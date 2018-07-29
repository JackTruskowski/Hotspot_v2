import os
import sqlite3
from flask import Flask
from flask import render_template
from flask import request
import db

app = Flask(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'instance', 'hotflask.sqlite')
USERNAME = "DefaultUser"

#the homepage for the application
@app.route('/temp')
def index():

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT restaurant.rname, restaurant.address, city.zipcode, city.cname, restaurant.rating, restaurant.price_range FROM restaurant INNER JOIN city on restaurant.zipcode=city.zipcode LIMIT 20;")
    data = cur.fetchall()
            
    return render_template('index.html', data=data)

@app.route('/star_desc')
def star_desc():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT restaurant.rname, restaurant.address, city.zipcode, city.cname, restaurant.rating, restaurant.price_range FROM restaurant INNER JOIN city on restaurant.zipcode=city.zipcode ORDER BY -restaurant.rating ASC LIMIT 20;")
    data = cur.fetchall()
            
    return render_template('index.html', data=data)

@app.route('/user', methods=['GET', 'POST'])
def userPage():
    
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
    if request.method == 'POST':
        cur.execute("INSERT INTO likes VALUES (?, ?)", (request.form['id'], USERNAME))
        conn.commit()

    cur.execute("SELECT x.rname, x.address, x.zipcode, city.cname, x.rating, x.price_range FROM (SELECT *  FROM restaurant r INNER JOIN likes ON r.rest_id=likes.restaurant_id)x INNER JOIN city ON x.zipcode=city.zipcode ;")
    
    data = cur.fetchall()
    return render_template('user.html', data=data, user=USERNAME)


@app.route('/', methods=['GET', 'POST'])
def defaultPage():

    # User is filtering
    if request.method == 'POST':
        try:
            rating_low = float(request.form['minrating'])
        except:
            rating_low = None

        try:
            rating_high = float(request.form['maxrating'])
        except:
            rating_high = None

        try:
            price_range = request.form['pricerange']
        except:
            price_range = None

        try:
            zipcode = request.form['zipcode']
        except:
            zipcode = None
        
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        query = db.do_query(rating_low, rating_high, price_range, zipcode)
        print(query)
        cur.execute(query)
        data = cur.fetchall()
        return render_template('index.html', data=data)

    # Default data
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT restaurant.rname, restaurant.address, city.zipcode, city.cname, restaurant.rating, restaurant.price_range, restaurant.rest_id FROM restaurant INNER JOIN city on restaurant.zipcode=city.zipcode ;")
    data = cur.fetchall()

    return render_template('index.html', data=data)
