# setup_db.py
import sqlite3

conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

# Drop the old table if it exists (optional)
cursor.execute("DROP TABLE IF EXISTS employees")

# Create new table
cursor.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    department TEXT,
    salary TEXT,
    address TEXT
)
""")

# Add 5 sample employees
sample_data = [
    ("Peter Smith", 35, "Sales", "50000", "Main road, London"),
    ("Alice Johnson", 29, "Engineering", "75000", "123 Elm St, New York, NY"),
    ("Catherine Lee", 41, "Finance", "85000", "789 Pine Rd, Chicago, IL"),
    ("Raj Patel", 38, "Marketing", "62000", "67 Queen St, Toronto"),
    ("Sara Ahmed", 30, "HR", "56000", "44 King Ave, Dubai")
]

cursor.executemany("INSERT INTO employees (name, age, department, salary, address) VALUES (?, ?, ?, ?, ?)", sample_data)

conn.commit()
conn.close()

print("Database initialized with sample data.")
