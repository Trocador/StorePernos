# database/connection.py

import sqlite3
from contextlib import contextmanager
from config.settings import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn):
    with open("database/schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
