# tests/conftest.py
import pytest
import sqlite3

@pytest.fixture
def test_conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    with open("database/schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    yield conn
    conn.close()