from datetime import date, timedelta

from etl.db import get_source_connection, get_target_connection


def get_transaction_date_range(source_conn):
    cursor = source_conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                MIN(DATE(start_time)) AS min_date,
                MAX(DATE(end_time)) AS max_date
            FROM transactions
        """)

        result = cursor.fetchone()

        return result["min_date"], result["max_date"]

    finally:
        cursor.close()


def load_dim_date():
    source_conn = None
    target_conn = None
    target_cursor = None

    try:
        # Connect to source MySQL database
        source_conn = get_source_connection()
        print("MySQL connection: OK")

        # Connect to target PostgreSQL database
        target_conn = get_target_connection()
        target_cursor = target_conn.cursor()

        print("PostgreSQL connection: OK")

        # Determine required date range from transaction data
        min_date, max_date = get_transaction_date_range(source_conn)

        print(f"Transaction date range: {min_date} to {max_date}")

        if min_date is None or max_date is None:
            raise ValueError("No transaction dates found in source database")

        # Clean target dimension for repeatable learning-stage loads
        target_cursor.execute("""
            TRUNCATE TABLE dim_date
        """)

        insert_sql = """
            INSERT INTO dim_date (
                date_key,
                full_date,
                year,
                quarter,
                month,
                month_name,
                week,
                day,
                day_name,
                is_weekend
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        current_date = min_date
        row_count = 0

        while current_date <= max_date:
            date_key = int(current_date.strftime("%Y%m%d"))
            year = current_date.year
            quarter = ((current_date.month - 1) // 3) + 1
            month = current_date.month
            month_name = current_date.strftime("%B")
            week = current_date.isocalendar().week
            day = current_date.day
            day_name = current_date.strftime("%A")
            is_weekend = current_date.weekday() >= 5

            target_cursor.execute(
                insert_sql,
                (
                    date_key,
                    current_date,
                    year,
                    quarter,
                    month,
                    month_name,
                    week,
                    day,
                    day_name,
                    is_weekend,
                ),
            )

            row_count += 1
            current_date += timedelta(days=1)

        target_conn.commit()

        print(f"PostgreSQL dim_date loaded: {row_count}")
        print("dim_date load completed successfully")

    except Exception as exc:
        if target_conn:
            target_conn.rollback()

        print(f"dim_date load failed: {exc}")
        raise

    finally:
        if target_cursor:
            target_cursor.close()

        if source_conn:
            source_conn.close()

        if target_conn:
            target_conn.close()

        print("Connections closed")


if __name__ == "__main__":
    load_dim_date()