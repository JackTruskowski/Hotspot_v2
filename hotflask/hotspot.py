import os
import sqlite3
from flask import Flask
from flask import render_template
from flask import request
from flask_login import current_user
from flask_login import LoginManager
import db

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'instance', 'hotflask.sqlite')
USERNAME = "Default"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['POST', 'GET'])
def loginPage():

    if request.method == 'POST':

        if(request.form.get("newaccount") != None):
            user = db.add_user(request.form.get("username"), request.form.get("password"))
        else:
            user = db.get_user(request.form.get("username"), request.form.get("password"))
            
        if not user:
            return render_template('login.html', error="Failed to authenticate.")
        else:
            USERNAME = user[0]
            return render_template('index.html', data=db.get_default_data())

    return render_template('login.html', error=None)

@app.route('/user', methods=['GET', 'POST'])
def userPage():
    
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
    if request.method == 'POST':
        cur.execute("INSERT INTO likes VALUES (?, ?)", (request.form['id'], USERNAME))
        conn.commit()

    cur.execute("SELECT x.rname, x.address, x.zipcode, city.cname, x.rating, x.price_range FROM (SELECT *  FROM restaurant r INNER JOIN likes ON r.rest_id=likes.restaurant_id)x INNER JOIN city ON x.zipcode=city.zipcode LIMIT 100;")
    
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
        
        data = db.do_query(rating_low, rating_high, price_range, zipcode)
        return render_template('index.html', data=data)


    # Default data
    data = db.get_default_data()

    return render_template('index.html', data=data)

@app.route('/search', methods=['GET', 'POST'])
def searchPage():
    if request.method == 'POST':
        try:
            search_term = request.form['search']
        except:
            search_term = None
            
        if search_term != None:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT restaurant.rname, restaurant.address, city.zipcode, city.cname, restaurant.rating, restaurant.price_range, restaurant.rest_id FROM restaurant INNER JOIN city on restaurant.zipcode=city.zipcode WHERE restaurant.rname LIKE \"%" + search_term + "%\" LIMIT 100;")
            data = cur.fetchall()
        else:
            data = db.get_default_data()

        return render_template('index.html', data=data)

