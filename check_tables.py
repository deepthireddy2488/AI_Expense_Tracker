from dotenv import load_dotenv
load_dotenv()

from database.db import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
""")

print("Tables:", cursor.fetchall())

cursor.execute("SELECT COUNT(*) FROM users;")
print("Users count:", cursor.fetchone()[0])

cursor.close()
connection.close()