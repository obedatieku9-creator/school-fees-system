import argparse
import os
import sqlite3
import sys

try:
    import psycopg2
except ImportError:
    psycopg2 = None


def connect_sqlite(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"SQLite file not found: {path}")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def connect_postgres(dsn):
    if psycopg2 is None:
        raise RuntimeError('psycopg2 is required to run this migration script')
    return psycopg2.connect(dsn)


def ensure_postgres_schema(conn):
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'admin'
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                section TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                student_id TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                gender TEXT NOT NULL,
                date_of_birth DATE NOT NULL,
                class_id INTEGER NOT NULL REFERENCES classes(id),
                parent_name TEXT NOT NULL,
                parent_phone TEXT NOT NULL,
                address TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fees_structure (
                id SERIAL PRIMARY KEY,
                class_id INTEGER NOT NULL REFERENCES classes(id),
                term TEXT NOT NULL,
                amount REAL NOT NULL,
                UNIQUE(class_id, term)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                student_id TEXT NOT NULL,
                amount REAL NOT NULL,
                term TEXT NOT NULL,
                payment_date DATE NOT NULL,
                payment_method TEXT NOT NULL,
                receipt_number TEXT UNIQUE NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (student_id)
            )
        ''')
    conn.commit()


def copy_users(sqlite_conn, pg_conn):
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute('SELECT username, password_hash, role FROM users')
    rows = sqlite_cursor.fetchall()
    with pg_conn.cursor() as cursor:
        for row in rows:
            cursor.execute('''
                INSERT INTO users (username, password_hash, role)
                VALUES (%s, %s, %s)
                ON CONFLICT (username) DO UPDATE SET password_hash = EXCLUDED.password_hash, role = EXCLUDED.role
            ''', (row['username'], row['password_hash'], row['role']))
    pg_conn.commit()
    return len(rows)


def copy_classes(sqlite_conn, pg_conn):
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute('SELECT name, section FROM classes')
    rows = sqlite_cursor.fetchall()
    with pg_conn.cursor() as cursor:
        for row in rows:
            cursor.execute('''
                INSERT INTO classes (name, section)
                VALUES (%s, %s)
                ON CONFLICT (name) DO UPDATE SET section = EXCLUDED.section
            ''', (row['name'], row['section']))
    pg_conn.commit()
    return len(rows)


def class_id_map(pg_conn):
    with pg_conn.cursor() as cursor:
        cursor.execute('SELECT id, name FROM classes')
        return {row[1]: row[0] for row in cursor.fetchall()}


def copy_students(sqlite_conn, pg_conn):
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute('SELECT student_id, full_name, gender, date_of_birth, class_id, parent_name, parent_phone, address FROM students')
    rows = sqlite_cursor.fetchall()
    name_map = class_id_map(pg_conn)

    with pg_conn.cursor() as cursor:
        for row in rows:
            sqlite_cursor.execute('SELECT name FROM classes WHERE id = ?', (row['class_id'],))
            class_row = sqlite_cursor.fetchone()
            if not class_row:
                raise RuntimeError(f"Class id {row['class_id']} not found in SQLite classes")
            class_name = class_row['name']
            pg_class_id = name_map.get(class_name)
            if pg_class_id is None:
                raise RuntimeError(f"Postgres class not found for {class_name}")
            cursor.execute('''
                INSERT INTO students (student_id, full_name, gender, date_of_birth, class_id, parent_name, parent_phone, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (student_id) DO UPDATE SET
                    full_name = EXCLUDED.full_name,
                    gender = EXCLUDED.gender,
                    date_of_birth = EXCLUDED.date_of_birth,
                    class_id = EXCLUDED.class_id,
                    parent_name = EXCLUDED.parent_name,
                    parent_phone = EXCLUDED.parent_phone,
                    address = EXCLUDED.address
            ''', (
                row['student_id'],
                row['full_name'],
                row['gender'],
                row['date_of_birth'],
                pg_class_id,
                row['parent_name'],
                row['parent_phone'],
                row['address']
            ))
    pg_conn.commit()
    return len(rows)


def copy_fees(sqlite_conn, pg_conn):
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute('SELECT class_id, term, amount FROM fees_structure')
    rows = sqlite_cursor.fetchall()
    with pg_conn.cursor() as cursor:
        for row in rows:
            sqlite_cursor.execute('SELECT name FROM classes WHERE id = ?', (row['class_id'],))
            class_row = sqlite_cursor.fetchone()
            if not class_row:
                raise RuntimeError(f"Class id {row['class_id']} not found in SQLite classes")
            class_name = class_row['name']
            pg_class_id = class_id_map(pg_conn).get(class_name)
            if pg_class_id is None:
                raise RuntimeError(f"Postgres class not found for {class_name}")
            cursor.execute('''
                INSERT INTO fees_structure (class_id, term, amount)
                VALUES (%s, %s, %s)
                ON CONFLICT (class_id, term) DO UPDATE SET amount = EXCLUDED.amount
            ''', (pg_class_id, row['term'], row['amount']))
    pg_conn.commit()
    return len(rows)


def copy_payments(sqlite_conn, pg_conn):
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute('SELECT student_id, amount, term, payment_date, payment_method, receipt_number FROM payments')
    rows = sqlite_cursor.fetchall()
    with pg_conn.cursor() as cursor:
        for row in rows:
            cursor.execute('''
                INSERT INTO payments (student_id, amount, term, payment_date, payment_method, receipt_number)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (receipt_number) DO NOTHING
            ''', (
                row['student_id'],
                row['amount'],
                row['term'],
                row['payment_date'],
                row['payment_method'],
                row['receipt_number']
            ))
    pg_conn.commit()
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description='Migrate SQLite school_fees.db data into PostgreSQL')
    parser.add_argument('--sqlite', default=os.path.join('database', 'school_fees.db'), help='Path to the old SQLite database file')
    parser.add_argument('--postgres', default=os.environ.get('DATABASE_URL'), help='Postgres DATABASE_URL connection string')
    args = parser.parse_args()

    if not args.postgres:
        parser.error('Postgres URL must be provided via --postgres or DATABASE_URL environment variable')

    sqlite_conn = connect_sqlite(args.sqlite)
    pg_conn = connect_postgres(args.postgres)

    try:
        ensure_postgres_schema(pg_conn)
        print('Postgres schema ensured.')

        n_users = copy_users(sqlite_conn, pg_conn)
        n_classes = copy_classes(sqlite_conn, pg_conn)
        n_students = copy_students(sqlite_conn, pg_conn)
        n_fees = copy_fees(sqlite_conn, pg_conn)
        n_payments = copy_payments(sqlite_conn, pg_conn)

        print(f'Migration complete: {n_users} users, {n_classes} classes, {n_students} students, {n_fees} fees, {n_payments} payments copied.')
    finally:
        sqlite_conn.close()
        pg_conn.close()


if __name__ == '__main__':
    main()
