CREATE SCHEMA IF NOT EXISTS STG;
DROP SCHEMA IF EXISTS public;

-- staging DB
CREATE TABLE IF NOT EXISTS STG.department (
    department_id int PRIMARY KEY,
    department_name varchar(50)
);

CREATE TABLE IF NOT EXISTS STG.aisle (
    aisle_id int PRIMARY KEY,
    aisle_name VARCHAR(50),
    department_id int NOT NULL,
    FOREIGN KEY (department_id) REFERENCES STG.department(department_id)  
);

CREATE TABLE IF NOT EXISTS STG.product (
    product_id int PRIMARY KEY,
    product_name varchar(200),
    aisle_id int NOT NULL,
    FOREIGN key (aisle_id) REFERENCES STG.aisle(aisle_id)
);

CREATE TABLE IF NOT EXISTS STG.driver (  -- no user table -> no driver table?
    driver_id int PRIMARY KEY,
    driver_tip decimal(10,2),
    tip boolean
);

CREATE TABLE IF NOT EXISTS STG.orders (
    order_id int PRIMARY KEY,
    order_dt timestamp,
    user_id int, -- no user table -> no driver table?
    driver_id int,
    FOREIGN KEY (driver_id) REFERENCES STG.driver(driver_id),  -- no user table -> no driver table?
    tip boolean
);

CREATE TABLE IF NOT EXISTS STG.order_product (
    order_id int,
    FOREIGN key (order_id) REFERENCES STG.orders(order_id),
    product_id int,
    FOREIGN KEY (product_id) REFERENCES STG.product(product_id),
    PRIMARY KEY (order_id, product_id)
);
