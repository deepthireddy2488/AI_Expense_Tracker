from database.db import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
SELECT *
FROM budgets
ORDER BY budget_id;
""")

rows = cursor.fetchall()

print(rows)

cursor.close()
connection.close()