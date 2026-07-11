from database.db import get_connection

def get_user_by_email(email):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE email = %s
    """, (email,))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user

def register_user(full_name, email, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO users (full_name, email, password)
    VALUES (%s, %s, %s)
    """, (full_name, email, password))

    connection.commit()

    cursor.close()
    connection.close()