-- Create the procedure to compute the average weighted score for a user
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT DEFAULT 0;
    DECLARE weighted_score_sum FLOAT DEFAULT 0;
    
    -- Calculate the sum of weighted scores and total weight
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO weighted_score_sum, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    -- If total_weight is greater than 0, calculate the average weighted score
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
    
END $$

DELIMITER ;
