-- ============================================================
-- EVCharge BI - PostgreSQL Star Schema
-- Target database: PostgreSQL
-- ============================================================

-- ------------------------------------------------------------
-- Dimension: Date
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    week INTEGER NOT NULL,
    day INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL
);


-- ------------------------------------------------------------
-- Dimension: Operator
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dim_operator (
    operator_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    operator_id INTEGER NOT NULL,
    operator_code VARCHAR(20) NOT NULL,
    operator_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL
);


-- ------------------------------------------------------------
-- Dimension: Location
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dim_location (
    location_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    location_id INTEGER NOT NULL,
    operator_id INTEGER NOT NULL,
    location_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    latitude NUMERIC(10,7),
    longitude NUMERIC(10,7),
    location_type VARCHAR(30) NOT NULL,
    status VARCHAR(20) NOT NULL
);


-- ------------------------------------------------------------
-- Dimension: Charge Point
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dim_charge_point (
    charge_point_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    charge_point_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    charge_point_code VARCHAR(30) NOT NULL,
    connector_type VARCHAR(20) NOT NULL,
    power_kw NUMERIC(6,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    commissioned_at TIMESTAMP
);


-- ------------------------------------------------------------
-- Dimension: Customer
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    customer_code VARCHAR(20) NOT NULL,
    customer_name VARCHAR(150) NOT NULL,
    email VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100),
    created_at TIMESTAMP
);


-- ------------------------------------------------------------
-- Fact: Charging
-- Grain:
-- One row = one EV charging session / transaction
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS fact_charging (
    charging_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    date_key INTEGER NOT NULL,
    operator_key INTEGER NOT NULL,
    location_key INTEGER NOT NULL,
    charge_point_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,

    transaction_code VARCHAR(30) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,

    duration_minutes INTEGER NOT NULL,
    energy_kwh NUMERIC(12,3) NOT NULL,
    amount NUMERIC(12,2) NOT NULL,

    status VARCHAR(20) NOT NULL
);