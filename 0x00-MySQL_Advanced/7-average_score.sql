-- Active: 1695137323808@@127.0.0.1@3306@holberton
-- SQL script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student.
-- Note: An average score can be a decimal
-- Requirements:
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value.

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)


BEGIN
UPDATE users
SET average_score = (
    SELECT AVG(score) FROM corrections
    WHERE corrections.user_id = user_id
)
WHERE id = user_id;

END $$

DELIMITER ;
