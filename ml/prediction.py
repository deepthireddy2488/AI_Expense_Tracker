import pandas as pd
from sklearn.linear_model import LinearRegression
from database.db import get_connection


def predict_next_month_expense(user_id):

    connection = get_connection()

    query = """
        SELECT
            EXTRACT(MONTH FROM expense_date) AS month,
            SUM(amount) AS total
        FROM expenses
        WHERE user_id=%s
        GROUP BY EXTRACT(MONTH FROM expense_date)
        ORDER BY month
    """

    df = pd.read_sql(query, connection, params=(user_id,))

    connection.close()

    if len(df) < 2:
        return 0

    X = df[['month']]
    y = df['total']

    model = LinearRegression()
    model.fit(X, y)

    next_month = [[df['month'].max() + 1]]

    prediction = model.predict(next_month)

    return round(float(prediction[0]), 2)


from datetime import datetime

from datetime import datetime

def save_prediction(user_id, predicted_expense):

    connection = get_connection()
    cursor = connection.cursor()

    now = datetime.now()

    month = now.month
    year = now.year

    cursor.execute("""
        SELECT prediction_id
        FROM predictions
        WHERE user_id=%s
        AND prediction_month=%s
        AND prediction_year=%s
    """, (user_id, month, year))

    result = cursor.fetchone()

    if result:

        cursor.execute("""
            UPDATE predictions
            SET predicted_expense=%s,
                created_at=CURRENT_TIMESTAMP
            WHERE prediction_id=%s
        """, (predicted_expense, result[0]))

    else:

        cursor.execute("""
            INSERT INTO predictions
            (user_id, prediction_month, prediction_year, predicted_expense)
            VALUES (%s,%s,%s,%s)
        """, (
            user_id,
            month,
            year,
            predicted_expense
        ))

    connection.commit()

    cursor.close()
    connection.close()