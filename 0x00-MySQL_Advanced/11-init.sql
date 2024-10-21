-- Initial
DROP TABLE IF EXISTS students;

CREATE TABLE IF NOT EXISTS students (
    name VARCHAR(255) NOT NULL,
    score INT default 0,
    last_meeting DATE NULL 
);

INSERT INTO students (name, score) VALUES ("Bob", 80);
INSERT INTO students (name, score) VALUES ("Sylvia", 120);
INSERT INTO students (name, score) VALUES ("Jean", 60);
INSERT INTO students (name, score) VALUES ("Steeve", 50);
INSERT INTO students (name, score) VALUES ("Camilia", 80);
INSERT INTO students (name, score) VALUES ("Alexa", 130);

-- Create the `need_meeting` view
CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80
  AND (last_meeting IS NULL OR last_meeting < CURDATE() - INTERVAL 1 MONTH);

-- Test the `need_meeting` view by selecting data from it
SELECT * FROM need_meeting;

-- Update Bob's score to be less than 80 and check the view
UPDATE students SET score = 40 WHERE name = 'Bob';
SELECT * FROM need_meeting;

-- Update Steeve's score to 80 and check the view
UPDATE students SET score = 80 WHERE name = 'Steeve';
SELECT * FROM need_meeting;

-- Set Jean's last meeting date to today and check the view
UPDATE students SET last_meeting = CURDATE() WHERE name = 'Jean';
SELECT * FROM need_meeting;

-- Set Jean's last meeting date to 2 months ago and check the view
UPDATE students SET last_meeting = ADDDATE(CURDATE(), INTERVAL -2 MONTH) WHERE name = 'Jean';
SELECT * FROM need_meeting;

-- Show the SQL that creates the `need_meeting` view
SHOW CREATE VIEW need_meeting;

-- Show the SQL that creates the `students` table
SHOW CREATE TABLE students;
