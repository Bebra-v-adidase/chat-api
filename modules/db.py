import sqlite3

def create_tables():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category INTEGER,
            priority INTEGER,
            messages JSON,
            employee_id INTEGER,
            use_bot BOOLEAN DEFAULT TRUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50),
            categories_competence JSON
        )
    ''')

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect("db.sqlite")
