import sqlite3

Database = sqlite3.connect('main.db')
cur = Database.cursor()
users = (cur.execute("SELECT * FROM users;").fetchall())

print(users)
