import sqlite3
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.append(project_root)

conn = sqlite3.connect(os.path.join(parent_dir, 'database', 'db.sqlite3'))
cursor = conn.cursor()

fonc = cursor.execute('select * from Fonctionnaire')

fonc = cursor.fetchall()


print(fonc[1][0])

