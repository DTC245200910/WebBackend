CREATE DATABASE IF NOT EXISTS product_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE product_db;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DOUBLE NOT NULL,
    quantity INT NOT NULL
);

INSERT INTO products (name, price, quantity) VALUES
('Laptop Dell XPS 13', 25000000, 10),
('iPhone 15 Pro', 28000000, 15),
('Bàn phím cơ Keychron K2', 2200000, 30);
