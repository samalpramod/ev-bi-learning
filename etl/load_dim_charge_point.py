from etl.db import get_source_connection, get_target_connection


# ---------------------------------------------------------
# Load dim_charge_point
# ---------------------------------------------------------
def load_dim_charge_point(mysql_conn, postgres_conn):
    mysql_cursor = mysql_conn.cursor(dictionary=True)

    mysql_cursor.execute("""
        SELECT
            id,
            location_id,
            charge_point_code,
            connector_type,
            power_kw,
            status,
            commissioned_at
        FROM charge_points
        ORDER BY id
    """)

    charge_points = mysql_cursor.fetchall()

    print(f"MySQL charge points found: {len(charge_points)}")

    pg_cursor = postgres_conn.cursor()

    # Start clean for this learning ETL.
    # Later we will replace this with incremental/upsert logic.
    pg_cursor.execute(
        "TRUNCATE TABLE dim_charge_point RESTART IDENTITY"
    )

    insert_sql = """
        INSERT INTO dim_charge_point
        (
            charge_point_id,
            location_id,
            charge_point_code,
            connector_type,
            power_kw,
            status,
            commissioned_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for charge_point in charge_points:
        pg_cursor.execute(
            insert_sql,
            (
                charge_point["id"],
                charge_point["location_id"],
                charge_point["charge_point_code"],
                charge_point["connector_type"],
                charge_point["power_kw"],
                charge_point["status"],
                charge_point["commissioned_at"],
            ),
        )

    postgres_conn.commit()

    print(
        f"PostgreSQL dim_charge_point loaded: "
        f"{len(charge_points)}"
    )

    mysql_cursor.close()
    pg_cursor.close()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():
    mysql_conn = None
    postgres_conn = None

    try:
        mysql_conn = get_source_connection()
        print("MySQL connection: OK")

        postgres_conn = get_target_connection()
        print("PostgreSQL connection: OK")

        load_dim_charge_point(mysql_conn, postgres_conn)

        print("dim_charge_point load completed successfully")

    except Exception as error:
        if postgres_conn:
            postgres_conn.rollback()

        print(f"ETL failed: {error}")
        raise

    finally:
        if mysql_conn:
            mysql_conn.close()

        if postgres_conn:
            postgres_conn.close()

        print("Connections closed")


if __name__ == "__main__":
    main()