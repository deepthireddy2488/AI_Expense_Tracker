import os
import psycopg2


def get_connection():

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url)

    return psycopg2.connect(
        host="localhost",
        database="ai_expense_tracker",
        user="postgres",
        password="dfordatabase",
        port="5432"
    )