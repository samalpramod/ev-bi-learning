from etl.db import get_source_connection, get_target_connection


# ---------------------------------------------------------
# Load dim_location
# ---------------------------------------------------------
def load_dim_location(mysql_conn, postgres_conn):
    mysql_cursor = mysql_conn.cursor(dictionary=True)

    mysql_cursor.execute("""
        SELECT
            id,
            operator_id,
            name,
            city,
            state,
            latitude,
            longitude,
            location_type,
            status
        FROM locations
        ORDER BY id
    """)

    locations = mysql_cursor.fetchall()

    print(f"MySQL locations found: {len(locations)}")

    pg_cursor = postgres_conn.cursor()

    # Start clean for this learning ETL.
    # Later we will replace this with incremental/upsert logic.
    pg_cursor.execute("TRUNCATE TABLE dim_location RESTART IDENTITY")

    insert_sql = """
        INSERT INTO dim_location
        (
            location_id,
            operator_id,
            location_name,
            city,
            state,
            latitude,
            longitude,
            location_type,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for location in locations:
        pg_cursor.execute(
            insert_sql,
            (
                location["id"],
                location["operator_id"],
                location["name"],
                location["city"],
                location["state"],
                location["latitude"],
                location["longitude"],
                location["location_type"],
                location["status"],
            ),
        )

    postgres_conn.commit()

    print(f"PostgreSQL dim_location loaded: {len(locations)}")

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

        load_dim_location(mysql_conn, postgres_conn)

        print("dim_location load completed successfully")

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