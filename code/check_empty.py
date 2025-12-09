import sqlite3
import os

db_path = os.path.join('database', 'db.sqlite3')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
total_rows = 0
print("Row counts:")
for t in tables:
    name = t[0]
    if name == 'sqlite_sequence': continue
    cursor.execute(f"SELECT COUNT(*) FROM {name}")
    count = cursor.fetchone()[0]
    print(f"- {name}: {count}")
    total_rows += count

conn.close()

if total_rows == 0:
    print("SUCCESS: Database is empty.")
else:
    print(f"FAILURE: Database has {total_rows} rows.")
