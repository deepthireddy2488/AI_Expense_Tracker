from database.db import get_connection


def add_expense(user_id, category_id, amount, payment_method, expense_date, description):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (user_id, category_id, amount, payment_method, expense_date, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """,
    (
        user_id,
        category_id,
        amount,
        payment_method,
        expense_date,
        description
    ))

    connection.commit()

    cursor.close()
    connection.close()

def get_user_expenses(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            e.expense_id,
            c.category_name,
            e.amount,
            e.payment_method,
            e.expense_date,
            e.description

        FROM expenses e

        JOIN categories c
            ON e.category_id = c.category_id

        WHERE e.user_id = %s

        ORDER BY e.expense_date DESC
    """, (user_id,))

    expenses = cursor.fetchall()

    cursor.close()
    connection.close()

    return expenses

def get_expense_by_id(expense_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            expense_id,
            category_id,
            amount,
            payment_method,
            expense_date,
            description

        FROM expenses

        WHERE expense_id = %s
    """, (expense_id,))

    expense = cursor.fetchone()

    cursor.close()
    connection.close()

    return expense



def update_expense(
    expense_id,
    category_id,
    amount,
    payment_method,
    expense_date,
    description
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses

        SET
            category_id = %s,
            amount = %s,
            payment_method = %s,
            expense_date = %s,
            description = %s

        WHERE expense_id = %s
    """,
    (
        category_id,
        amount,
        payment_method,
        expense_date,
        description,
        expense_id
    ))

    connection.commit()

    cursor.close()
    connection.close()


def delete_expense(expense_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE expense_id = %s
    """, (expense_id,))

    connection.commit()

    cursor.close()
    connection.close()




def get_all_expenses(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.category_name,
            e.amount,
            e.payment_method,
            e.expense_date

        FROM expenses e

        JOIN categories c
        ON e.category_id = c.category_id

        WHERE e.user_id = %s

        ORDER BY e.expense_date DESC
    """, (user_id,))

    expenses = cursor.fetchall()

    cursor.close()
    connection.close()

    return expenses


