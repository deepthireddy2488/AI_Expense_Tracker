from database.db import get_connection
from datetime import datetime


def get_dashboard_data(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    # Total Income
    cursor.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM income
        WHERE user_id=%s
    """,(user_id,))
    total_income = cursor.fetchone()[0]

    # Total Expense
    cursor.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM expenses
        WHERE user_id=%s
    """,(user_id,))
    total_expense = cursor.fetchone()[0]

    balance = total_income - total_expense

    cursor.close()
    connection.close()

    return (
    round(total_income, 2),
    round(total_expense, 2),
    round(balance, 2)
)





def get_category_expense(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.category_name,
            SUM(e.amount)

        FROM expenses e

        JOIN categories c
        ON e.category_id=c.category_id

        WHERE e.user_id=%s

        GROUP BY c.category_name
    """,(user_id,))

    data=cursor.fetchall()

    cursor.close()
    connection.close()

    return data





def get_monthly_expense(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            TO_CHAR(expense_date,'Mon'),
            SUM(amount)

        FROM expenses

        WHERE user_id=%s

        GROUP BY
            EXTRACT(MONTH FROM expense_date),
            TO_CHAR(expense_date,'Mon')

        ORDER BY
            EXTRACT(MONTH FROM expense_date)
    """,(user_id,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data




def get_budget(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(MAX(budget_amount),0)
        FROM budgets
        WHERE user_id=%s
    """, (user_id,))

    budget = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return budget




def get_budget_details(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            month,
            year,
            budget_amount
        FROM budgets
        WHERE user_id=%s
        ORDER BY budget_id DESC
        LIMIT 1
    """, (user_id,))

    budget = cursor.fetchone()

    cursor.close()
    connection.close()

    return budget 










def get_recent_transactions(user_id):

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
        LIMIT 5
    """, (user_id,))

    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return transactions





def get_budget_percentage(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(MAX(budget_amount),0)
        FROM budgets
        WHERE user_id=%s
    """, (user_id,))

    budget = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM expenses
        WHERE user_id=%s
    """, (user_id,))

    expense = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    if budget == 0:
        return 0

    percentage = (expense / budget) * 100

    return round(percentage, 2)





def generate_insight(budget_percentage):

    if budget_percentage == 0:
        return "No budget has been set."

    elif budget_percentage < 70:
        return "✅ You are spending within your budget."

    elif budget_percentage < 90:
        return "⚠️ You are close to reaching your budget."

    else:
        return "🚨 Warning! You have exceeded or are about to exceed your budget."
    



    
def save_insight(user_id, insight):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO insights
        (user_id, insight_text)
        VALUES (%s, %s)
    """, (user_id, insight))

    connection.commit()

    cursor.close()
    connection.close()





def highest_expense_category(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.category_name,
            SUM(e.amount) AS total

        FROM expenses e

        JOIN categories c
        ON e.category_id = c.category_id

        WHERE e.user_id = %s

        GROUP BY c.category_name

        ORDER BY total DESC

        LIMIT 1
    """, (user_id,))

    data = cursor.fetchone()

    cursor.close()
    connection.close()

    if data:
        return data[0]
    else:
        return "No Expenses"


def detect_anomaly(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.category_name,
            e.amount
        FROM expenses e
        JOIN categories c
            ON e.category_id = c.category_id
        WHERE e.user_id = %s
        ORDER BY e.amount DESC
        LIMIT 1
    """, (user_id,))

    expense = cursor.fetchone()

    cursor.close()
    connection.close()

    if expense is None:
        return None

    category = expense[0]
    amount = float(expense[1])

    if amount > 5000:
        return f"🚨 Unusual expense detected! You spent ₹{amount} on {category}."

    return None




def predict_next_month_expense(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT amount
        FROM expenses
        WHERE user_id=%s
        ORDER BY expense_date
    """, (user_id,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    if len(data) == 0:
        return 0

    total = 0

    for row in data:
        total += float(row[0])

    prediction = total / len(data)

    return round(prediction, 2)




from datetime import datetime

def save_prediction(user_id, predicted_expense):

    connection = get_connection()
    cursor = connection.cursor()

    month = datetime.now().month
    year = datetime.now().year

    cursor.execute("""
        INSERT INTO predictions
        (
            user_id,
            prediction_month,
            prediction_year,
            predicted_expense
        )

        VALUES
        (%s,%s,%s,%s)

    """, (
        user_id,
        month,
        year,
        predicted_expense
    ))

    connection.commit()

    cursor.close()
    connection.close()

