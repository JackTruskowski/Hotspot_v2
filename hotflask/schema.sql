DROP TABLE IF EXISTS restaurant;

CREATE TABLE restaurant (
    rest_id int PRIMARY KEY,
    rating real,
    name text,
    address text,
    phone text,
    website text,
    price_range int,
    years_open int,
    category string
);
