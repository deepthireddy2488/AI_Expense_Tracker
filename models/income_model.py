from database.db import get_connection


def add_income(user_id, amount, source, income_date, description):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO income
        (user_id, amount, source, income_date, description)
        VALUES (%s, %s, %s, %s, %s)
    """,
    (
        user_id,
        amount,
        source,
        income_date,
        description
    ))

    connection.commit()

    cursor.close()
    connection.close()


def get_user_income(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            income_id,
            amount,
            source,
            income_date,
            description
        FROM income
        WHERE user_id=%s
        ORDER BY income_date DESC
    """,(user_id,))

    income = cursor.fetchall()

    cursor.close()
    connection.close()

    return income


def get_income_by_id(income_id):

    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute("""
        SELECT
            income_id,
            amount,
            source,
            income_date,
            description
        FROM income
        WHERE income_id=%s
    """,(income_id,))

    income=cursor.fetchone()

    cursor.close()
    connection.close()

    return income


def update_income(income_id,amount,source,income_date,description):

    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute("""
        UPDATE income
        SET
            amount=%s,
            source=%s,
            income_date=%s,
            description=%s
        WHERE income_id=%s
    """,
    (
        amount,
        source,
        income_date,
        description,
        income_id
    ))

    connection.commit()

    cursor.close()
    connection.close()


def delete_income(income_id):

    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute("""
        DELETE FROM income
        WHERE income_id=%s
    """,(income_id,))

    connection.commit()

    cursor.close()
    connection.close()