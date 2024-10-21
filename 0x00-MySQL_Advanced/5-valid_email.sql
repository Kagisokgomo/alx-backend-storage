DELIMITER //

CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;

//

DELIMITER ;

-- Initial setup
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    id int not null AUTO_INCREMENT,
    email varchar(255) not null,
    name varchar(255),
    valid_email boolean not null default 0,
    PRIMARY KEY (id)
);

-- Insert initial data
INSERT INTO users (email, name) VALUES ("bob@dylan.com", "Bob");
INSERT INTO users (email, name, valid_email) VALUES ("sylvie@dylan.com", "Sylvie", 1);
INSERT INTO users (email, name, valid_email) VALUES ("jeanne@dylan.com", "Jeanne", 1);

-- Create the trigger
DELIMITER $$

CREATE TRIGGER reset_valid_email_on_email_change
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Check if the email is being updated (i.e., it's different from the old value)
    IF OLD.email != NEW.email THEN
        -- Reset the valid_email field to 0 when the email changes
        SET NEW.valid_email = 0;
    END IF;
END $$

DELIMITER ;

-- Sample updates (email change and non-email change)
UPDATE users SET valid_email = 1 WHERE email = "bob@dylan.com";  -- No email change, valid_email should remain 1
UPDATE users SET email = "sylvie+new@dylan.com" WHERE email = "sylvie@dylan.com";  -- Email changed, valid_email should reset to 0
UPDATE users SET name = "Jannis" WHERE email = "jeanne@dylan.com";  -- No email change, valid_email should remain 1

-- Display the result after updates
SELECT * FROM users;

-- Trying to update with the same email (valid_email should not reset)
UPDATE users SET email = "bob@dylan.com" WHERE email = "bob@dylan.com";  -- No change in email, valid_email should stay as is

-- Display final state
SELECT * FROM users;
