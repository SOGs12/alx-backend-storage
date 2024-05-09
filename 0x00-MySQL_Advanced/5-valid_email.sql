DELIMITER //

-- Create the trigger
CREATE TRIGGER email_update_trigger
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0; -- Reset valid_email if email has changed
    END IF;
END //

DELIMITER ;
