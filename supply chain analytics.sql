CREATE DATABASE supply_chain_db;

CREATE WAREHOUSE supply_chain_wh
WITH WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE;

USE DATABASE supply_chain_db;
USE WAREHOUSE supply_chain_wh;

USE DATABASE supply_chain_db;
USE SCHEMA public;

CREATE STAGE supply_chain_stage;


CREATE TABLE products (
    product_id INT,
    product_name STRING,
    category STRING,
    cost_price FLOAT,
    selling_price FLOAT
);

CREATE TABLE warehouses (
    warehouse_id INT,
    warehouse_name STRING,
    location STRING
);

CREATE TABLE inventory (
    inventory_id INT,
    product_id INT,
    warehouse_id INT,
    stock_quantity INT,
    last_updated DATE
);

CREATE TABLE sales (
    sale_id INT,
    product_id INT,
    warehouse_id INT,
    quantity_sold INT,
    sale_date DATE
);

select top 5 * from sales
select top 5 * from warehouses
select top 5 * from products
select top 5 * from inventory
select count(*) from sales

--checking for duplicate products
SELECT product_id, COUNT(*)
FROM products
GROUP BY product_id
HAVING COUNT(*) > 1

--checking for duplicate sales
SELECT sale_id, COUNT(*)
FROM sales
GROUP BY sale_id
HAVING COUNT(*) > 1;

--checking null values
SELECT *
FROM products
WHERE product_id IS NULL
   OR product_name IS NULL
   OR cost_price IS NULL
   OR selling_price IS NULL;
SELECT *
FROM sales
WHERE product_id IS NULL
   OR warehouse_id IS NULL
   OR quantity_sold IS NULL;

SELECT *
FROM products
WHERE selling_price < cost_price;

SELECT *
FROM sales
WHERE quantity_sold <= 0;


SELECT *
FROM sales s
LEFT JOIN products p
ON s.product_id = p.product_id
WHERE p.product_id IS NULL;

CREATE OR REPLACE VIEW v_total_revenue AS
SELECT 
    SUM(s.quantity_sold * p.selling_price) AS total_revenue,
    SUM(s.quantity_sold) AS total_units_sold
FROM sales s
JOIN products p
ON s.product_id = p.product_id;

CREATE OR REPLACE VIEW v_warehouse_performance AS
SELECT 
    w.warehouse_id,
    w.warehouse_name,
    w.location,
    SUM(s.quantity_sold * p.selling_price) AS warehouse_revenue,
    SUM(s.quantity_sold) AS total_units_sold
FROM sales s
JOIN products p 
ON s.product_id = p.product_id
JOIN warehouses w
ON s.warehouse_id = w.warehouse_id
GROUP BY w.warehouse_id, w.warehouse_name, w.location;

CREATE OR REPLACE VIEW v_product_performance AS
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(s.quantity_sold) AS total_units_sold,
    SUM(s.quantity_sold * p.selling_price) AS total_revenue
FROM sales s
JOIN products p
ON s.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category;

CREATE OR REPLACE VIEW v_stock_turnover AS
SELECT 
    p.product_id,
    p.product_name,
    SUM(s.quantity_sold) / NULLIF(AVG(i.stock_quantity), 0) AS stock_turnover
FROM sales s
JOIN products p 
ON s.product_id = p.product_id
JOIN inventory i 
ON s.product_id = i.product_id
GROUP BY p.product_id, p.product_name;

SELECT * FROM v_total_revenue;
SELECT * FROM v_warehouse_performance ORDER BY warehouse_revenue DESC;








