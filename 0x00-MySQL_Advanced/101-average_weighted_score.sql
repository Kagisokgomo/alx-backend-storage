-- Change delimiter to define the procedure
DELIMITER $$

-- Create procedure to compute average weighted score for all users
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;
    DECLARE total_weight INT;
    DECLARE weighted_score_sum FLOAT;
    
    -- Declare cursor to iterate through all users
    DECLARE user_cursor CURSOR FOR
        SELECT id FROM users;
    
    -- Declare handler for end of cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    -- Open the cursor
    OPEN user_cursor;
    
    -- Loop through all users
    read_loop: LOOP
        FETCH user_cursor INTO user_id;
        
        -- Exit the loop if all users have been processed
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Initialize total_weight and weighted_score_sum for each user
        SET total_weight = 0;
        SET weighted_score_sum = 0;
        
        -- Calculate the sum of weighted scores and total weight for the user
        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO weighted_score_sum, total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;
        
        -- If total_weight is greater than 0, compute and update average score
        IF total_weight > 0 THEN
            UPDATE users
            SET average_score = weighted_score_sum / total_weight
            WHERE id = user_id;
        ELSE
            -- If no projects, set average_score to 0
            UPDATE users
            SET average_score = 0
            WHERE id = user_id;
        END IF;
    END LOOP;
    
    -- Close the cursor
    CLOSE user_cursor;
END $$

-- Reset delimiter to default
DELIMITER ;
