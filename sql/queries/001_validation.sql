SELECT COUNT(*) FROM operators;

SELECT COUNT(*) FROM locations;

SELECT COUNT(*) FROM charge_points;

SELECT COUNT(*) FROM customers;

SELECT COUNT(*) FROM transactions;

SELECT COUNT(*) FROM payments;

SELECT
    MIN(start_time) AS first_transaction,
    MAX(start_time) AS last_transaction
FROM transactions;

SELECT
    status,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY status;

SELECT
    payment_method,
    COUNT(*) AS count
FROM payments
GROUP BY payment_method;

