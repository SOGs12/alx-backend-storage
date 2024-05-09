-- Active: 1695137323808@@127.0.0.1@3306@holberton
-- Write a SQL script that creates a trigger
-- trigger decreases the quantity of an item after adding a new order.
-- Quantity in the table items can be negative.

CREATE TRIGGER quantity_update AFTER INSERT ON orders
FOR EACH ROW
UPDATE items
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;
