from dotenv import load_dotenv
load_dotenv()

from database.db import get_connection

connection = get_connection()
cursor = connection.cursor()

# Users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Categories
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE NOT NULL
);
""")

# Income
cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    income_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    source VARCHAR(100),
    income_date DATE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Expenses
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    expense_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(category_id),
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50),
    expense_date DATE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Default categories
cursor.execute("""
INSERT INTO categories (category_name)
VALUES
('Food'),
('Travel'),
('Shopping'),
('Bills'),
('Healthcare'),
('Education'),
('Entertainment'),
('Other')
ON CONFLICT (category_name) DO NOTHING;
""")


connection.commit()

cursor.execute("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public';
""")

print(cursor.fetchall())

cursor.close()
connection.close()

print("Done")