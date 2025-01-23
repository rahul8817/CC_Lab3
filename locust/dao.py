import json
import os
import sqlite3


DB_PATH = 'carts.db'


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if not os.path.exists(DB_PATH):
        create_tables(conn)
    return conn


def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            contents TEXT DEFAULT '[]',
            cost REAL DEFAULT 0
        )
    ''')
    conn.commit()


def get_cart(username: str) -> list:
    with connect() as conn:
        cursor = conn.execute('SELECT * FROM carts WHERE username = ?', (username,))
        return [dict(row) for row in cursor.fetchall()]


def add_to_cart(username: str, product_id: int):
    with connect() as conn:
        cursor = conn.execute('SELECT contents FROM carts WHERE username = ?', (username,))
        row = cursor.fetchone()
        contents = json.loads(row['contents']) if row else []
        contents.append(product_id)

        conn.execute('''
            INSERT INTO carts (username, contents, cost)
            VALUES (?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET
            contents = excluded.contents
        ''', (username, json.dumps(contents), 0))
        conn.commit()


def remove_from_cart(username: str, product_id: int):
    with connect() as conn:
        cursor = conn.execute('SELECT contents FROM carts WHERE username = ?', (username,))
        row = cursor.fetchone()
        if not row:
            return

        contents = json.loads(row['contents'])
        if product_id in contents:
            contents.remove(product_id)

        conn.execute('''
            INSERT INTO carts (username, contents, cost)
            VALUES (?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET
            contents = excluded.contents
        ''', (username, json.dumps(contents), 0))
        conn.commit()


def delete_cart(username: str):
    with connect() as conn:
        conn.execute('DELETE FROM carts WHERE username = ?', (username,))
        conn.commit()