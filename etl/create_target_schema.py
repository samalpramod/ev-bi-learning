from pathlib import Path

from etl.db import get_target_connection


def main():
    schema_file = (
        Path(__file__).resolve().parent.parent
        / "sql"
        / "schema"
        / "postgres_star_schema.sql"
    )

    sql = schema_file.read_text(encoding="utf-8")

    connection = get_target_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)

        connection.commit()
        print("PostgreSQL BI schema created successfully")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
        print("PostgreSQL connection closed")


if __name__ == "__main__":
    main()