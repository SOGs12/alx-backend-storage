-- Active: 1695137323808@@127.0.0.1@3306@holberton
--  a SQL script that creates a table users requirements


CREATE TABLE IF NOT EXISTS users(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country ENUM('US', 'CO','TN') DEFAULT 'US' NOT NULL
);
