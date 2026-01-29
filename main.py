# main.py (fragmento) database inicialization
from database.connection import get_connection
from utils.db import create_connection
import sqlite3
from ui.app import App

def init_db():
    with get_connection() as conn:
        with open("database/schema.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())

def conn_factory():
    conn = sqlite3.connect("TiendaPernos.db")
    conn.row_factory = sqlite3.Row   # filas accesibles por nombre
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

if __name__ == "__main__":
    App(conn_factory).mainloop()
