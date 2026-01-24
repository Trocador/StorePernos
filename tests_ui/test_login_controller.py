# tests_ui/test_login_controller.py
import pytest
import sqlite3
from database import init_schema
from ui.login_controller import LoginController

class DummyConn:
    def __enter__(self): return self
    def __exit__(self, *args): pass

def conn_factory_stub():
    conn = sqlite3.connect(":memory:")
    init_schema(conn)   # crea tablas
    return conn

def login_ok_stub(conn, usuario, password):
    return {"usuario": usuario, "id_usuario": 1}

def login_fail_stub(conn, usuario, password):
    return None

def test_login_success():
    logged = {"user": None}
    def on_success(u): logged["user"] = u

    controller = LoginController(
        login_fn=login_ok_stub,
        conn_factory=conn_factory_stub,
        on_success=on_success
    )

    ok = controller.login("admin", "1234")
    assert ok is True
    assert logged["user"]["usuario"] == "admin"

def test_login_failure():
    logged = {"user": None}
    def on_success(u): logged["user"] = u

    controller = LoginController(
        login_fn=login_fail_stub,
        conn_factory=conn_factory_stub,
        on_success=on_success
    )

    ok = controller.login("admin", "wrong")
    assert ok is False
    assert logged["user"] is None