DROP TABLE IF EXISTS restaurant;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS reservation;
DROP TABLE IF EXISTS likes;


CREATE TABLE restaurant (
       rest_id int PRIMARY KEY,
       rating real,
       rname text,
       address text,
       phone text,
       website text,
       price_range int,
       years_open int,
       category string,
       zipcode text,
       UNIQUE (rname, address),
       UNIQUE (rname, phone)
);

CREATE TABLE city (
       zipcode int PRIMARY KEY,
       state text,
       cname text,
       neighborhood text
);

CREATE TABLE user (
       username text PRIMARY KEY,
       password text
);

CREATE TABLE reservation (
       reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
       username text,
       date text,
       rest_id text,
       time text
);

CREATE TABLE likes (
       restaurant_id int,
       username text,
       PRIMARY KEY(restaurant_id, username)
);
