# main.py (fragmento) database inicialization
from database.connection import get_connection
import sqlite3
from ui.app import App

def init_db():
    with get_connection() as conn:
        with open("database/schema.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())

def conn_factory():
    return sqlite3.connect("TiendaPernos.db")

if __name__ == "__main__":
    App(conn_factory).mainloop()
