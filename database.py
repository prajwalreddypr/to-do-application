import sqlite3


conn = sqlite3.connect('todo.db')
c = conn.cursor()


c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0
    )
''')


conn.commit()
conn.close()

print("Database and table created.")
