from database.db import get_connection


def get_all_categories():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category_id, category_name
        FROM categories
        ORDER BY category_name
    """)

    categories = cursor.fetchall()

    cursor.close()
    connection.close()

    return categories