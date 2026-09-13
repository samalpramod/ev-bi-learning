CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    week INT NOT NULL,
    day INT NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL
);
CREATE TABLE dim_operator (
    operator_key INT AUTO_INCREMENT PRIMARY KEY,
    operator_id INT NOT NULL,
    operator_code VARCHAR(20) NOT NULL,
    operator_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL
);

CREATE TABLE dim_location (
    location_key INT AUTO_INCREMENT PRIMARY KEY,
    location_id INT NOT NULL,
    operator_id INT NOT NULL,
    location_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    location_type VARCHAR(30) NOT NULL,
    status VARCHAR(20) NOT NULL
);

CREATE TABLE dim_charge_point (
    charge_point_key INT AUTO_INCREMENT PRIMARY KEY,
    charge_point_id INT NOT NULL,
    location_id INT NOT NULL,
    charge_point_code VARCHAR(30) NOT NULL,
    connector_type VARCHAR(20) NOT NULL,
    power_kw DECIMAL(6,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    commissioned_at DATETIME
);

CREATE TABLE dim_customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    customer_code VARCHAR(20) NOT NULL,
    customer_name VARCHAR(150) NOT NULL,
    email VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100),
    created_at DATETIME
);

CREATE TABLE fact_charging (
    charging_key BIGINT AUTO_INCREMENT PRIMARY KEY,

    date_key INT NOT NULL,
    operator_key INT NOT NULL,
    location_key INT NOT NULL,
    charge_point_key INT NOT NULL,
    customer_key INT NOT NULL,

    transaction_code VARCHAR(30) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,

    duration_minutes INT NOT NULL,
    energy_kwh DECIMAL(12,3) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,

    status VARCHAR(20) NOT NULL
);

CREATE TABLE fact_charging (
    charging_key BIGINT AUTO_INCREMENT PRIMARY KEY,

    date_key INT NOT NULL,
    operator_key INT NOT NULL,
    location_key INT NOT NULL,
    charge_point_key INT NOT NULL,
    customer_key INT NOT NULL,

    transaction_code VARCHAR(30) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,

    duration_minutes INT NOT NULL,
    energy_kwh DECIMAL(12,3) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,

    status VARCHAR(20) NOT NULL
);