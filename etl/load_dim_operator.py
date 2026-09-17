import mysql.connector
from etl.db import get_source_connection, get_target_connection

# ---------------------------------------------------------
# Load dim_operator
# ---------------------------------------------------------
def load_dim_operator(mysql_conn, postgres_conn):
    mysql_cursor = mysql_conn.cursor(dictionary=True)

    mysql_cursor.execute("""
        SELECT
            id as operator_id,
            code as operator_code,
            name as operator_name,
            status
        FROM operators
        ORDER BY operator_id
    """)

    operators = mysql_cursor.fetchall()

    print(f"MySQL operators found: {len(operators)}")

    pg_cursor = postgres_conn.cursor()

    # Start clean for this learning ETL.
    # Later we will replace this with incremental/upsert logic.
    pg_cursor.execute("TRUNCATE TABLE dim_operator RESTART IDENTITY")

    insert_sql = """
        INSERT INTO dim_operator
        (
            operator_id,
            operator_code,
            operator_name,
            status
        )
        VALUES (%s, %s, %s, %s)
    """

    for operator in operators:
        pg_cursor.execute(
            insert_sql,
            (
                operator["operator_id"],
                operator["operator_code"],
                operator["operator_name"],
                operator["status"]
            ),
        )

    postgres_conn.commit()

    print(f"PostgreSQL dim_operator loaded: {len(operators)}")

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

        load_dim_operator(mysql_conn, postgres_conn)

        print("dim_operator load completed successfully")

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