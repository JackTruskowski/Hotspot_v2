import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def do_query(min_rating, max_rating, price_range, zipcode):
    query = "SELECT restaurant.rname, restaurant.address, city.zipcode, city.cname, restaurant.rating, restaurant.price_range FROM restaurant INNER JOIN city on restaurant.zipcode=city.zipcode"
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

        
        
    #query += " LIMIT 20;"
    return query
    
    

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')    


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
