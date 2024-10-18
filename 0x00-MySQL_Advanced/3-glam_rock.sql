-- Create a new table to store the lifespan of each band
CREATE TABLE IF NOT EXISTS glam_rock_bands AS
SELECT 
    band_name,
    (2022 - formed) - IF(split IS NULL, 0, (2022 - split)) AS lifespan
FROM 
    metal_bands
WHERE 
    style = 'Glam Rock';

-- Select and rank the bands based on their lifespan
SELECT 
    band_name,
    lifespan
FROM 
    glam_rock_bands
ORDER BY 
    lifespan DESC;
