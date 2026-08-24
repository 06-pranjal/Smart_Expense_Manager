import sqlite3
import pandas as pd

DB_NAME = "expenses.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_transaction(date, transaction_type, category, amount, description):
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO transactions
        (date, transaction_type, category, amount, description)
        VALUES (?, ?, ?, ?, ?)
    """, (date, transaction_type, category, amount, description))

    conn.commit()
    conn.close()


def get_transactions():
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM transactions ORDER BY date DESC",
        conn
    )

    conn.close()

    return df


def delete_transaction(transaction_id):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    conn.commit()
    conn.close()