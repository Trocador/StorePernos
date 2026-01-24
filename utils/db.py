# utils/db.py
import sqlite3
from config.settings import DB_PATH

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

class SafeConnection:
    """
    Context manager seguro para conexiones SQLite.
    Devuelve un objeto sqlite3.Connection real en __enter__.
    Maneja commit, rollback y cierre en __exit__.
    """

    def __init__(self, conn_factory=None):
        self.conn_factory = conn_factory or create_connection
        self.conn = None

    def _default_factory(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def __enter__(self):
        # 🔥 Aquí devolvemos la conexión real
        self.conn = self.conn_factory()
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
        finally:
            self.conn.close()