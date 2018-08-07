import sqlite3
import os
import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash, check_password_hash

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'instance', 'hotflask.sqlite')

'''
Creates a connection to the database
'''
def connect():
    conn = sqlite3.connect(DATABASE)
    cur=conn.cursor()
    return cur

'''
Adds a user to the database
TODO: enforce unique username
'''
def add_user(username, password):

    pw_hash = generate_password_hash(password)
    
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO user VALUES (?, ?)", (username, pw_hash))
        conn.commit()
        cur.execute("SELECT * FROM user WHERE username LIKE \"" + username + "\"")
        data = cur.fetchone()
        
        if data and check_salted_password(password, data[1]):
            return data
        else:
            return None
        
    except:
        return None

    
def check_salted_password(plaintext, salted):
    return check_password_hash(salted, plaintext)

'''
Tries to return the corresponding user given a username and password
'''
def get_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE username LIKE \"" + username + "\"")
    data = cur.fetchone()

    if data and check_salted_password(password, data[1]):
        return data
    else:
        return None


'''
Returns a restaurant given its ID
'''
def get_restaurant(rest_id):
    cur = connect()
    try:
        cur.execute("SELECT * FROM restaurant WHERE rest_id LIKE \"" + rest_id + "\"")
        data = cur.fetchone()
        return data
    except Exception as e:
        print(e)
        return None

'''
Given a username, pulls their likes and reservations from the relevant tables
'''    
def get_user_likes_and_reservations(username):

    cur = connect()
    cur.execute("SELECT x.rname, x.address, x.zipcode, city.cname, x.rating, x.price_range, x.restaurant_id FROM (SELECT *  FROM restaurant r INNER JOIN likes ON (r.rest_id=likes.restaurant_id AND likes.username LIKE \"" + username + "\"))x INNER JOIN city ON x.zipcode=city.zipcode LIMIT 100;")
    data = cur.fetchall()

    
    cur.execute("SELECT restaurant.rname, x.date, x.time, x.reservation_id FROM restaurant INNER JOIN (SELECT * FROM reservation r INNER JOIN user ON r.username=user.username WHERE user.username LIKE \"" + username + "\")x ON restaurant.rest_id=x.rest_id")
    res = cur.fetchall()
    print(data)
    print(res)

    return (data, res)

    
'''
Pulls some default data from the database (just the first 100 rows)
'''    
def get_default_data():
    cur = connect()
    cur.execute("SELECT restaurant.rname, restaurant.address, city.zipcode, city.cname, restaurant.rating, restaurant.price_range, restaurant.rest_id FROM restaurant INNER JOIN city on restaurant.zipcode=city.zipcode LIMIT 100;")
    return(cur.fetchall())


'''
Used for filtering, takes a number of filter parameters and builds and executes the query
'''
def do_query(min_rating, max_rating, price_range, zipcode):
    cur = connect()
    query = "SELECT restaurant.rname, restaurant.address, city.zipcode, city.cname, restaurant.rating, restaurant.price_range, restaurant.rest_id FROM restaurant INNER JOIN city on restaurant.zipcode=city.zipcode"
    if min_rating or max_rating or price_range or zipcode:
        query += " WHERE "
    if min_rating:
        query += "restaurant.rating >= " + str(min_rating)
    if max_rating:
        if min_rating:
            query += " AND "
        query += "restaurant.rating <= " + str(max_rating)
    if price_range:
        if min_rating or max_rating:
            query += " AND "
        query += "restaurant.price_range LIKE \"" + price_range + "\""
    if zipcode:
        try:
            zip_code = int(zipcode)
            if min_rating or max_rating or price_range:
                query += " AND "
            query += "restaurant.zipcode LIKE \"" + str(zip_code) + "\""
        except:
            print("invalid zip code")

    query += " LIMIT 100 ;"
        
    #query += " LIMIT 20;"
    cur.execute(query)
    return cur.fetchall()
    
