-- Active: 1695137323808@@127.0.0.1@3306@hbtn_0d_tvshows
-- a SQL script that creates a table users following requirements

CREATE TABLE IF NOT EXISTS users(
    id INT UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
