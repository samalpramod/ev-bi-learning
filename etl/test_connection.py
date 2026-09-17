from etl.db import get_source_connection, get_target_connection


def main():
    source_conn = get_source_connection()
    target_conn = get_target_connection()

    print("Source database connection: OK")
    print("Target database connection: OK")

    source_conn.close()
    target_conn.close()

    print("Connections closed successfully")


if __name__ == "__main__":
    main()