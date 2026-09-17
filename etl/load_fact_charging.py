from etl.db import get_source_connection, get_target_connection


def load_fact_charging():
    source_conn = None
    target_conn = None
    source_cursor = None
    target_cursor = None

    try:
        # Connect to source MySQL database
        source_conn = get_source_connection()
        source_cursor = source_conn.cursor(dictionary=True)

        print("MySQL connection: OK")

        # Connect to target PostgreSQL database
        target_conn = get_target_connection()
        target_cursor = target_conn.cursor()

        print("PostgreSQL connection: OK")

        # Read transactions and resolve warehouse dimension keys
        source_cursor.execute("""
            SELECT
                t.transaction_code,
                t.charge_point_id,
                t.customer_id,
                t.start_time,
                t.end_time,
                t.duration_minutes,
                t.energy_kwh,
                t.amount,
                t.status,
                cp.location_id,
                l.operator_id
            FROM transactions t
            INNER JOIN charge_points cp
                ON t.charge_point_id = cp.id
            INNER JOIN locations l
                ON cp.location_id = l.id
            ORDER BY t.id
        """)

        transactions = source_cursor.fetchall()

        print(f"MySQL transactions found: {len(transactions)}")

        # Clean target fact table for repeatable learning-stage loads
        target_cursor.execute("""
            TRUNCATE TABLE fact_charging RESTART IDENTITY
        """)

        insert_sql = """
            INSERT INTO fact_charging (
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
                d.date_key,
                o.operator_key,
                l.location_key,
                cp.charge_point_key,
                c.customer_key,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            FROM dim_date d
            INNER JOIN dim_operator o
                ON o.operator_id = %s
            INNER JOIN dim_location l
                ON l.location_id = %s
            INNER JOIN dim_charge_point cp
                ON cp.charge_point_id = %s
            INNER JOIN dim_customer c
                ON c.customer_id = %s
            WHERE d.full_date = %s
        """

        for transaction in transactions:
            start_time = transaction["start_time"]
            start_date = start_time.date()

            target_cursor.execute(
                insert_sql,
                (
                    transaction["transaction_code"],
                    transaction["start_time"],
                    transaction["end_time"],
                    transaction["duration_minutes"],
                    transaction["energy_kwh"],
                    transaction["amount"],
                    transaction["status"],
                    transaction["operator_id"],
                    transaction["location_id"],
                    transaction["charge_point_id"],
                    transaction["customer_id"],
                    start_date,
                ),
            )

        target_conn.commit()

        # Verify target count
        target_cursor.execute("""
            SELECT COUNT(*)
            FROM fact_charging
        """)

        target_count = target_cursor.fetchone()[0]

        print(f"PostgreSQL fact_charging loaded: {target_count}")

        if target_count != len(transactions):
            raise ValueError(
                f"Row count mismatch: source={len(transactions)}, "
                f"target={target_count}"
            )

        print("fact_charging load completed successfully")

    except Exception as exc:
        if target_conn:
            target_conn.rollback()

        print(f"fact_charging load failed: {exc}")
        raise

    finally:
        if source_cursor:
            source_cursor.close()

        if target_cursor:
            target_cursor.close()

        if source_conn:
            source_conn.close()

        if target_conn:
            target_conn.close()

        print("Connections closed")


if __name__ == "__main__":
    load_fact_charging()