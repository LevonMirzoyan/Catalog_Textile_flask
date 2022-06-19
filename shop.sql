PRAGMA foreign_keys=on;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS producer;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    producer_id INTEGER NOT NULL,
    FOREIGN KEY (producer_id) REFERENCES producer(id)
);

CREATE TABLE IF NOT EXISTS producer (
    id INTEGER PRIMARY KEY ,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    producer_country TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY ,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
);
