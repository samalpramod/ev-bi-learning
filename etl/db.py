import mysql.connector
import psycopg

from etl.config import SOURCE_DB, TARGET_DB


def get_source_connection():
    """Create a connection to the MySQL OLTP database."""
    return mysql.connector.connect(**SOURCE_DB)


def get_target_connection():
    """Create a connection to the PostgreSQL BI database."""
    return psycopg.connect(**TARGET_DB)