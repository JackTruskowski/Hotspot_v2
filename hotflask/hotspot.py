import os
import sqlite3
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, session, flash
from flask_login import current_user
from flask_login import LoginManager
from functools import wraps
import db
import random
import string

app = Flask(__name__)

#generate a random string to use for the secrety key
app.secret_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'instance', 'hotflask.sqlite')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('loginPage'))

@app.route('/', methods=['GET', 'POST'])
def defaultPage():

    if not 'user' in session:
        return redirect(url_for('loginPage'))

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
            session['logged_in'] = True
            session['user'] = request.form.get("username")
            return redirect(url_for('defaultPage'))
        #return render_template('index.html', data=db.get_default_data())

    return render_template('login.html', error=None)

@app.route('/userLike', methods=['GET', 'POST'])
def userPage():

    if not 'user' in session:
        return redirect(url_for('loginPage'))
    
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
    if request.method == 'POST':
        cur.execute("INSERT INTO likes VALUES (?, ?)", (request.form['id'], session['user']))
        conn.commit()

    result = db.get_user_likes_and_reservations(session['user'])
    
    return render_template('user.html', data=result[0], res=result[1], user=session['user'])

@app.route('/userRes', methods=['GET', 'POST'])
def userRes():

    if not 'user' in session:
        return redirect(url_for('loginPage'))
    
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    if request.method == 'POST':
        date = request.form['res_date']
        restaurant = request.form['res'][1:-1].split(',')
        restaurant[0] = int(restaurant[0])
        time = request.form['time']
        cur.execute("INSERT INTO reservation (username, date, rest_id, time) VALUES (?, ?, ?, ?)", (session['user'], date, restaurant[0], time))
        conn.commit()

    result = db.get_user_likes_and_reservations(session['user'])
    
    return render_template('user.html', data=result[0], res=result[1], user=session['user'])

'''
Deletes a restaurant entry from the likes table
'''
@app.route('/likeDelete', methods=['POST'])
def likeDelete():

    if not 'user' in session:
        return redirect(url_for('loginPage'))
    
    like_to_delete = request.form['like']

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("DELETE FROM likes WHERE restaurant_id=" + like_to_delete + " AND username LIKE \"" + session['user'] + "\" ;")
    conn.commit()

    result = db.get_user_likes_and_reservations(session['user'])
    return render_template('user.html', data=result[0], res=result[1], user=session['user'])

'''
Deletes a reservation entry from the reservation table
'''
@app.route('/resDelete', methods=['POST'])
def resDelete():

    if not 'user' in session:
        return redirect(url_for('loginPage'))
    
    res_to_delete = request.form['res']

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("DELETE FROM reservation WHERE reservation_id=" + res_to_delete + " AND username LIKE \"" + session['user'] + "\" ;")
    conn.commit()

    result = db.get_user_likes_and_reservations(session['user'])
    return render_template('user.html', data=result[0], res=result[1], user=session['user'])


@app.route('/makereservation', methods=['POST'])
def makeReservation():

    if not 'user' in session:
        return redirect(url_for('loginPage'))
    
    try:
        rest_id = request.form['id']
        restaurant = db.get_restaurant(rest_id)
    except:
        return redirect(url_for('defaultPage'))
    return render_template('reservation.html', restaurant=restaurant, user=session['user'])


@app.route('/search', methods=['GET', 'POST'])
def searchPage():

    if not 'user' in session:
        return redirect(url_for('loginPage'))
    
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

