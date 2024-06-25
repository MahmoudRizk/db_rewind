CREATE USER db_test WITH PASSWORD '12345678';

CREATE DATABASE test;

\c test;

CREATE TABLE posts(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT
);

INSERT INTO posts (name, description) VALUES ('post 1', 'description 1');