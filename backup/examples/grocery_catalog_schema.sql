-- Grocery Catalog Database Schema

-- Categories table
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

-- Items table
CREATE TABLE items (
    item_id VARCHAR(10) PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(category_id),
    item_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_item_name UNIQUE (item_name)
);

-- Packet sizes table
CREATE TABLE packet_sizes (
    packet_id SERIAL PRIMARY KEY,
    item_id VARCHAR(10) NOT NULL REFERENCES items(item_id),
    weight_grams INTEGER NOT NULL,
    price DECIMAL(10, 2),
    in_stock BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_item_weight UNIQUE (item_id, weight_grams)
);

-- Create indexes for better performance
CREATE INDEX idx_items_category ON items(category_id);
CREATE INDEX idx_packet_sizes_item ON packet_sizes(item_id);
CREATE INDEX idx_packet_sizes_weight ON packet_sizes(weight_grams);

-- Sample insert statements for categories
INSERT INTO categories (category_name) VALUES 
('Fruits'),
('Vegetables'),
('Dairy'),
('Bakery'),
('Meat'),
('Seafood'),
('Grains'),
('Canned Goods'),
('Snacks'),
('Beverages'),
('Condiments'),
('Spices'),
('Frozen Foods'),
('Household'),
('Personal Care');

-- Sample insert statements for items and packet sizes
-- These would be generated from the CSV file
-- Example:
-- INSERT INTO items (item_id, category_id, item_name) 
-- VALUES ('F0001', (SELECT category_id FROM categories WHERE category_name = 'Fruits'), 'Fresh Farms Watermelon');
--
-- INSERT INTO packet_sizes (item_id, weight_grams, price) 
-- VALUES ('F0001', 500, 3.99);
-- INSERT INTO packet_sizes (item_id, weight_grams, price) 
-- VALUES ('F0001', 1000, 6.99);

-- Create a view for easy querying of the complete catalog
CREATE VIEW catalog_view AS
SELECT 
    i.item_id,
    c.category_name,
    i.item_name,
    ps.weight_grams,
    ps.price,
    ps.in_stock
FROM 
    items i
JOIN 
    categories c ON i.category_id = c.category_id
JOIN 
    packet_sizes ps ON i.item_id = ps.item_id
ORDER BY 
    c.category_name, i.item_name, ps.weight_grams;

-- Create a function to get all packet sizes for a specific item
CREATE OR REPLACE FUNCTION get_item_packets(p_item_id VARCHAR)
RETURNS TABLE (
    weight_grams INTEGER,
    price DECIMAL(10, 2),
    in_stock BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ps.weight_grams,
        ps.price,
        ps.in_stock
    FROM 
        packet_sizes ps
    WHERE 
        ps.item_id = p_item_id
    ORDER BY 
        ps.weight_grams;
END;
$$ LANGUAGE plpgsql;

-- Create a function to search items by name
CREATE OR REPLACE FUNCTION search_items(search_term VARCHAR)
RETURNS TABLE (
    item_id VARCHAR,
    category_name VARCHAR,
    item_name VARCHAR,
    available_packets INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.item_id,
        c.category_name,
        i.item_name,
        COUNT(ps.packet_id)::INTEGER as available_packets
    FROM 
        items i
    JOIN 
        categories c ON i.category_id = c.category_id
    JOIN 
        packet_sizes ps ON i.item_id = ps.item_id
    WHERE 
        i.item_name ILIKE '%' || search_term || '%'
    GROUP BY
        i.item_id, c.category_name, i.item_name
    ORDER BY 
        i.item_name;
END;
$$ LANGUAGE plpgsql;
