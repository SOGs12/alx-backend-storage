DELIMITER //

-- Create the procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE average_score FLOAT;

    -- Declare cursor to loop through user IDs
    DECLARE cur CURSOR FOR
        SELECT id
        FROM users;

    -- Declare continue handler for cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN cur;

    -- Loop through each user ID
    user_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Calculate the total weighted score for the user
        SELECT SUM(c.score * p.weight)
        INTO total_score
        FROM corrections c
        INNER JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Calculate the total weight for the user's projects
        SELECT SUM(p.weight)
        INTO total_weight
        FROM corrections c
        INNER JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Calculate the average weighted score
        IF total_weight > 0 THEN
            SET average_score = total_score / total_weight;
        ELSE
            SET average_score = 0;
        END IF;

        -- Update the user's average_score in the users table
        UPDATE users
        SET average_score = average_score
        WHERE id = user_id;
    END LOOP;

    -- Close the cursor
    CLOSE cur;
END //

DELIMITER ;
