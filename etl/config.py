import os

from dotenv import load_dotenv


load_dotenv()


SOURCE_DB = {
    "host": os.getenv("SOURCE_DB_HOST"),
    "port": int(os.getenv("SOURCE_DB_PORT", "3306")),
    "database": os.getenv("SOURCE_DB_NAME"),
    "user": os.getenv("SOURCE_DB_USER"),
    "password": os.getenv("SOURCE_DB_PASSWORD"),
}


TARGET_DB = {
    "host": os.getenv("TARGET_DB_HOST"),
    "port": int(os.getenv("TARGET_DB_PORT", "5432")),
    "dbname": os.getenv("TARGET_DB_NAME"),
    "user": os.getenv("TARGET_DB_USER"),
    "password": os.getenv("TARGET_DB_PASSWORD"),
}