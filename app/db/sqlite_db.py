# app/db/sqlite_db.py

import sqlite3

DB_PATH = "data/railops.db"


def run_query(sql: str):
    """
    Exécute une requête SQL en lecture sur la base SQLite.
    Renvoie une liste de tuples (résultats bruts).
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    finally:
        conn.close()