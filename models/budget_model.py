from database.db import get_connection


def set_budget(user_id, month, year, budget_amount):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO budgets (user_id, month, year, budget_amount)
        VALUES (%s, %s, %s, %s)
    """, (
        user_id,
        month,
        year,
        budget_amount
    ))

    connection.commit()

    cursor.close()
    connection.close()


def get_budget(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT budget_id,
               month,
               year,
               budget_amount
        FROM budgets
        WHERE user_id = %s
        ORDER BY year DESC, month DESC
        LIMIT 1
    """, (user_id,))

    budget = cursor.fetchone()

    cursor.close()
    connection.close()

    return budget