import os
import sqlite3


def connect(path='products.db'):
    """Establish a database connection and create tables if not exist."""
    exists = os.path.exists(path)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    if not exists:
        create_tables(conn)
    return conn


def create_tables(conn):
    """Create the products table and seed initial data."""
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            cost REAL NOT NULL,
            qty INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    seed_data(conn)


def seed_data(conn):
    """Populate the database with initial product data."""
    initial_data = [
        ("Backpack", "A durable and stylish backpack for daily use.", 800.0, 10),
        ("Wireless Mouse", "A sleek and ergonomic wireless mouse with a long battery life.", 800.0, 20),
        ("Bluetooth Speaker", "A portable Bluetooth speaker with high-quality sound and deep bass.", 3000.0, 30),
        ("Laptop Stand", "An adjustable laptop stand for better posture and cooling.", 250.0, 15),
        ("Notebook", "A premium notebook with thick, high-quality paper.", 50.0, 50),
        # Add more product tuples here...
    ]
    conn.executemany('''
        INSERT INTO products (name, description, cost, qty)
        VALUES (?, ?, ?, ?)
    ''', initial_data)
    conn.commit()


def list_products():
    """Fetch all products from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return products


def get_product(product_id: int):
    """Fetch a specific product by ID."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return dict(product) if product else None


def add_product(product: dict):
    """Insert a new product into the database."""
    conn = connect()
    conn.execute('INSERT INTO products (name, description, cost, qty) VALUES (?, ?, ?, ?)',
                 (product['name'], product['description'], product['cost'], product['qty']))
    conn.commit()
    conn.close()


def update_qty(product_id: int, qty: int):
    """Update the quantity of a product."""
    conn = connect()
    conn.execute('UPDATE products SET qty = ? WHERE id = ?', (qty, product_id))
    conn.commit()
    conn.close()


def delete_product(product_id: int):
    """Delete a product from the database."""
    conn = connect()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()


def update_product(product_id: int, product: dict):
    """Update product details."""
    conn = connect()
    conn.execute('''
        UPDATE products
        SET name = ?, description = ?, cost = ?, qty = ?
        WHERE id = ?
    ''', (product['name'], product['description'], product['cost'], product['qty'], product_id))
    conn.commit()
    conn.close()