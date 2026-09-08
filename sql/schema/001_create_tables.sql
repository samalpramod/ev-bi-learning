CREATE DATABASE evcharge_bi;

USE evcharge_bi;

CREATE TABLE operators (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    status ENUM('ACTIVE', 'INACTIVE') NOT NULL DEFAULT 'ACTIVE',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE locations (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    operator_id INT UNSIGNED NOT NULL,
    name VARCHAR(150) NOT NULL,
    city VARCHAR(80) NOT NULL,
    state VARCHAR(80) NOT NULL,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    location_type ENUM(
        'HIGHWAY',
        'MALL',
        'OFFICE',
        'RESIDENTIAL',
        'PUBLIC',
        'TRANSIT'
    ) NOT NULL,
    status ENUM('ACTIVE', 'INACTIVE') NOT NULL DEFAULT 'ACTIVE',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_locations_operator
        FOREIGN KEY (operator_id)
        REFERENCES operators(id)
);

CREATE TABLE charge_points (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    location_id INT UNSIGNED NOT NULL,
    charge_point_code VARCHAR(30) NOT NULL UNIQUE,
    connector_type ENUM('CCS2', 'TYPE2', 'CHADEMO') NOT NULL,
    power_kw DECIMAL(6,2) NOT NULL,
    status ENUM(
        'AVAILABLE',
        'CHARGING',
        'FAULTED',
        'OFFLINE'
    ) NOT NULL DEFAULT 'AVAILABLE',
    commissioned_at DATE NOT NULL,

    CONSTRAINT fk_charge_points_location
        FOREIGN KEY (location_id)
        REFERENCES locations(id)
);

CREATE TABLE customers (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    customer_code VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(150),
    city VARCHAR(80),
    state VARCHAR(80),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_code VARCHAR(40) NOT NULL UNIQUE,
    charge_point_id INT UNSIGNED NOT NULL,
    customer_id INT UNSIGNED NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    energy_kwh DECIMAL(10,3) NOT NULL,
    duration_minutes INT UNSIGNED NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    status ENUM(
        'COMPLETED',
        'CANCELLED',
        'FAILED'
    ) NOT NULL,

    CONSTRAINT fk_transactions_charge_point
        FOREIGN KEY (charge_point_id)
        REFERENCES charge_points(id),

    CONSTRAINT fk_transactions_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(id)
);

CREATE TABLE payments (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    payment_method ENUM(
        'UPI',
        'CARD',
        'WALLET',
        'NET_BANKING'
    ) NOT NULL,
    payment_status ENUM(
        'SUCCESS',
        'FAILED',
        'REFUNDED'
    ) NOT NULL,
    payment_time DATETIME NOT NULL,
    amount DECIMAL(12,2) NOT NULL,

    CONSTRAINT fk_payments_transaction
        FOREIGN KEY (transaction_id)
        REFERENCES transactions(id)
);