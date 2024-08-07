import sqlite3
import bcrypt

conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    content TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# Create admin user if not exists
cursor.execute('SELECT COUNT(*) FROM users WHERE username = "admin"')
if cursor.fetchone()[0] == 0:
    hashed = bcrypt.hashpw('john18'.encode('utf-8'), bcrypt.gensalt())
    cursor.execute('''
    INSERT INTO users (username, password, role)
    VALUES (?, ?, ?)
    ''', ('admin', hashed, 'admin'))

conn.commit()
conn.close()
