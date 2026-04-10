import sqlite3
import os
from werkzeug.security import generate_password_hash

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'school_fees.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'admin'
        )
    ''')

    # Classes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            section TEXT NOT NULL
        )
    ''')

    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            class_id INTEGER NOT NULL,
            parent_name TEXT NOT NULL,
            parent_phone TEXT NOT NULL,
            address TEXT NOT NULL,
            FOREIGN KEY (class_id) REFERENCES classes (id)
        )
    ''')

    # Fees structure table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fees_structure (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            term TEXT NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (class_id) REFERENCES classes (id),
            UNIQUE(class_id, term)
        )
    ''')

    # Payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            amount REAL NOT NULL,
            term TEXT NOT NULL,
            payment_date TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            receipt_number TEXT UNIQUE NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
    ''')

    # Insert default admin user
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    ''', ('admin', generate_password_hash('admin123'), 'admin'))  # Default password: admin123

    # Insert classes
    classes = [
        ('Foundation 1', 'Pre-School'),
        ('Foundation 2', 'Pre-School'),
        ('Reception 1', 'Pre-School'),
        ('Reception 2', 'Pre-School'),
        ('Primary 1', 'Primary School'),
        ('Primary 2', 'Primary School'),
        ('Primary 3', 'Primary School'),
        ('Primary 4', 'Primary School'),
        ('Primary 5', 'Primary School'),
        ('Primary 6', 'Primary School'),
        ('JHS 1', 'JHS'),
        ('JHS 2', 'JHS'),
        ('JHS 3', 'JHS')
    ]

    for name, section in classes:
        cursor.execute('INSERT OR IGNORE INTO classes (name, section) VALUES (?, ?)', (name, section))

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()