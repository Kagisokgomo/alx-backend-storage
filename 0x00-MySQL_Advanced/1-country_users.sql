-- This script creates a users table with unique email constraints and country enumeration

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- id as an auto-incrementing primary key
    email VARCHAR(255) NOT NULL UNIQUE,      -- email must be unique and cannot be null
    name VARCHAR(255),                        -- name can be null
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'  -- country with default value 'US'
);
