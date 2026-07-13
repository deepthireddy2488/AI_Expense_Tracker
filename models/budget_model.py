from database.db import get_connection

from database.db import get_connection

def set_budget(user_id, month, year, budget_amount):

    connection = get_connection()
    cursor = connection.cursor()

    # Check if budget already exists
    cursor.execute("""
        SELECT budget_id
        FROM budgets
        WHERE user_id=%s
        AND month=%s
        AND year=%s
    """, (user_id, month, year))

    budget = cursor.fetchone()

    if budget:

        # Update existing budget
        cursor.execute("""
            UPDATE budgets
            SET budget_amount=%s
            WHERE user_id=%s
            AND month=%s
            AND year=%s
        """, (
            budget_amount,
            user_id,
            month,
            year
        ))

    else:

        # Insert new budget
        cursor.execute("""
            INSERT INTO budgets
            (
                user_id,
                month,
                year,
                budget_amount
            )
            VALUES (%s,%s,%s,%s)
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
        SELECT budget_amount
        FROM budgets
        WHERE user_id=%s
        ORDER BY budget_id DESC
        LIMIT 1
    """, (user_id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return float(result[0])

    return 0