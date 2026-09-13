INSERT INTO fact_charging
(
    date_key,
    operator_key,
    location_key,
    charge_point_key,
    customer_key,

    transaction_code,
    start_time,
    end_time,

    duration_minutes,
    energy_kwh,
    amount,
    status
)
SELECT
    dd.date_key,
    do.operator_key,
    dl.location_key,
    dcp.charge_point_key,
    dc.customer_key,

    t.transaction_code,
    t.start_time,
    t.end_time,

    t.duration_minutes,
    t.energy_kwh,
    t.amount,
    t.status

FROM transactions t

JOIN dim_charge_point dcp
    ON t.charge_point_id = dcp.charge_point_id

JOIN dim_location dl
    ON dcp.location_id = dl.location_id

JOIN dim_operator do
    ON dl.operator_id = do.operator_id

JOIN dim_customer dc
    ON t.customer_id = dc.customer_id

JOIN dim_date dd
    ON DATE(t.start_time) = dd.full_date;