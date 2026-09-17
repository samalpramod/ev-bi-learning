from etl.db import get_source_connection, get_target_connection


def load_dim_customer():
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

        # Read customers from source
        source_cursor.execute("""
            SELECT
                id,
                customer_code,
                name,
                email,
                city,
                state,
                created_at
            FROM customers
            ORDER BY id
        """)

        customers = source_cursor.fetchall()

        print(f"MySQL customers found: {len(customers)}")

        # Clean target dimension for repeatable learning-stage loads
        target_cursor.execute("""
            TRUNCATE TABLE dim_customer RESTART IDENTITY
        """)

        # Insert into PostgreSQL dimension
        insert_sql = """
            INSERT INTO dim_customer (
                customer_id,
                customer_code,
                customer_name,
                email,
                city,
                state,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        for customer in customers:
            target_cursor.execute(
                insert_sql,
                (
                    customer["id"],
                    customer["customer_code"],
                    customer["name"],
                    customer["email"],
                    customer["city"],
                    customer["state"],
                    customer["created_at"],
                ),
            )

        target_conn.commit()

        print(f"PostgreSQL dim_customer loaded: {len(customers)}")
        print("dim_customer load completed successfully")

    except Exception as exc:
        if target_conn:
            target_conn.rollback()

        print(f"dim_customer load failed: {exc}")
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
    load_dim_customer()