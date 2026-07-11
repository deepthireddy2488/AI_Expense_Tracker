import psycopg2

def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="ai_expense_tracker",
        user="postgres",
        password="dfordatabase",
        port="5432"
    )
    return connection