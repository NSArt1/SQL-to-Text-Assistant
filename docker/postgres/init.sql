
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL
);
INSERT INTO customers (name, city) VALUES
    ('Alice', 'Amsterdam'),
    ('Bob', 'Paris'),
    ('Charlie', 'Amsterdam'),
    ('Diana', 'Berlin');

-- sales table
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    product_name TEXT NOT NULL,
    sales NUMERIC NOT NULL,
    sale_date DATE NOT NULL
);
INSERT INTO sales (product_id, product_name, sales, sale_date) VALUES
    (1, 'Widget', 1200, '2024-01-15'),
    (2, 'Gadget', 4100, '2024-02-20'),
    (1, 'Widget', 800,  '2024-02-10'),
    (3, 'Doohickey', 950, '2024-03-05');
