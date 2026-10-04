CREATE DATABASE STUZHA;
USE STUZHA;

CREATE TABLE customers (
    cust_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    phone BIGINT NOT NULL,
    city VARCHAR(20) NOT NULL
);

CREATE TABLE shipments (
    ship_id INT PRIMARY KEY AUTO_INCREMENT,
    track_no VARCHAR(15) UNIQUE NOT NULL,
    cust_id INT NOT NULL,
    receiver VARCHAR(30) NOT NULL,
    from_city VARCHAR(20) NOT NULL,
    to_city VARCHAR(20) NOT NULL,
    weight DECIMAL(5,2) NOT NULL,
    service ENUM('STANDARD','EXPRESS') NOT NULL,
    book_date DATE NOT NULL,
    status ENUM('BOOKED','IN TRANSIT','OUT FOR DELIVERY',
                'DELIVERED','CANCELLED') NOT NULL,
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id)
);

CREATE TABLE tracking (
    track_id INT PRIMARY KEY AUTO_INCREMENT,
    ship_id INT NOT NULL,
    place VARCHAR(30) NOT NULL,
    updated_on DATETIME NOT NULL,
    remark VARCHAR(50),
    FOREIGN KEY (ship_id) REFERENCES shipments(ship_id)
);

CREATE TABLE payments (
    pay_id INT PRIMARY KEY AUTO_INCREMENT,
    ship_id INT NOT NULL,
    amount DECIMAL(8,2) NOT NULL,
    mode ENUM('UPI','CARD','CASH') NOT NULL,
    status ENUM('PENDING','PAID') NOT NULL,
    FOREIGN KEY (ship_id) REFERENCES shipments(ship_id)
);

-- sample data
INSERT INTO customers (name, phone, city) VALUES
('Ramesh Sahu', 9876543210, 'Raipur'),
('Priya Verma', 9123456780, 'Bilaspur'),
('Amit Kumar', 9988776655, 'Korba');

INSERT INTO shipments (track_no, cust_id, receiver, from_city, to_city,
                       weight, service, book_date, status) VALUES
('TRK100001', 1, 'Sunita Sahu', 'Raipur', 'Delhi', 2.50, 'EXPRESS', '2026-09-28', 'IN TRANSIT'),
('TRK100002', 2, 'Rohit Verma', 'Bilaspur', 'Mumbai', 1.20, 'STANDARD', '2026-09-30', 'BOOKED');

INSERT INTO tracking (ship_id, place, updated_on, remark) VALUES
(1, 'Raipur', '2026-09-28 10:15:00', 'Shipment booked'),
(1, 'Nagpur', '2026-09-29 18:40:00', 'IN TRANSIT'),
(2, 'Bilaspur', '2026-09-30 11:05:00', 'Shipment booked');

INSERT INTO payments (ship_id, amount, mode, status) VALUES
(1, 150.00, 'UPI', 'PAID'),
(2, 74.00, 'CASH', 'PENDING');
