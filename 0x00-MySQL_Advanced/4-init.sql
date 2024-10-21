-- Initial setup
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS orders;

CREATE TABLE IF NOT EXISTS items (
    name VARCHAR(255) NOT NULL,
    quantity int NOT NULL DEFAULT 10
);

CREATE TABLE IF NOT EXISTS orders (
    item_name VARCHAR(255) NOT NULL,
    number int NOT NULL
);

-- Inserting sample data into items table
INSERT INTO items (name) VALUES ("apple"), ("pineapple"), ("pear");

-- Creating the trigger
DELIMITER $$

CREATE TRIGGER update_item_quantity
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    -- Update the quantity of the item in the items table by decreasing it
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END $$

DELIMITER ;

-- Sample orders
INSERT INTO orders (item_name, number) VALUES ('apple', 1);
INSERT INTO orders (item_name, number) VALUES ('apple', 3);
INSERT INTO orders (item_name, number) VALUES ('pear', 2);

-- Checking the result
SELECT * FROM items;
SELECT * FROM orders;
