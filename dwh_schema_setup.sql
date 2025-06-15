CREATE SCHEMA IF NOT EXISTS DWH;
DROP SCHEMA IF EXISTS public;

---- data warahouse DB
-- dimension product
CREATE TABLE IF NOT EXISTS DWH.product (
    product_id int PRIMARY KEY,
    product_name varchar(200),
    aisle_name varchar(50),
    department varchar (50)
);

-- fact orders
CREATE TABLE IF NOT EXISTS DWH.orders (
    order_id int,
    product_id int,
    order_dt timestamp,
    user_id int,
    driver_id int,
    tip boolean
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (product_id) REFERENCES DWH.product(product_id),
);