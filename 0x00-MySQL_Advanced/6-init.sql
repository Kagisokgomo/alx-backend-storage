-- Initial setup (creating tables and inserting sample data)
DROP TABLE IF EXISTS corrections;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS projects;

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    average_score FLOAT DEFAULT 0,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS projects (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS corrections (
    user_id INT NOT NULL,
    project_id INT NOT NULL,
    score INT DEFAULT 0,
    KEY `user_id` (`user_id`),
    KEY `project_id` (`project_id`),
    CONSTRAINT fk_user_id FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT fk_project_id FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE
);

-- Insert initial data into users and projects
INSERT INTO users (name) VALUES ("Bob");
SET @user_bob = LAST_INSERT_ID();

INSERT INTO users (name) VALUES ("Jeanne");
SET @user_jeanne = LAST_INSERT_ID();

INSERT INTO projects (name) VALUES ("C is fun");
SET @project_c = LAST_INSERT_ID();

INSERT INTO projects (name) VALUES ("Python is cool");
SET @project_py = LAST_INSERT_ID();

INSERT INTO corrections (user_id, project_id, score) VALUES (@user_bob, @project_c, 80);
INSERT INTO corrections (user_id, project_id, score) VALUES (@user_bob, @project_py, 96);

INSERT INTO corrections (user_id, project_id, score) VALUES (@user_jeanne, @project_c, 91);
INSERT INTO corrections (user_id, project_id, score) VALUES (@user_jeanne, @project_py, 73);

-- Create the AddBonus stored procedure
DELIMITER $$

CREATE PROCEDURE AddBonus (
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score INT
)
BEGIN
    DECLARE project_id INT;
    
    -- Check if the project already exists
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name
    LIMIT 1;
    
    -- If the project does not exist, insert it and get the new project_id
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;
    
    -- Insert the correction for the user and project
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);
    
END $$

DELIMITER ;

-- Example usage of the AddBonus stored procedure
CALL AddBonus((SELECT id FROM users WHERE name = "Jeanne"), "Python is cool", 100);
CALL AddBonus((SELECT id FROM users WHERE name = "Jeanne"), "Bonus project", 100);
CALL AddBonus((SELECT id FROM users WHERE name = "Bob"), "Bonus project", 10);
CALL AddBonus((SELECT id FROM users WHERE name = "Jeanne"), "New bonus", 90);

-- Show the updated data
SELECT * FROM projects;
SELECT * FROM corrections;
