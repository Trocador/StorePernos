# tests_ui/test_integration_flow.py
import sqlite3
import pytest
from ui.login_controller import LoginController
from ui.dashboard_controller import DashboardController
from database.repositories import usuarios_repo, productos_repo
from utils.security import hash_password
from services.auth_service import login

# --- Helper para DB en memoria ---
def conn_factory_memory(schema_path="database/schema.sql"):
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    return conn

# --- Test de integración ---
def test_full_flow_login_and_sale(monkeypatch):
    # 1. Prepara DB en memoria
    conn = conn_factory_memory()
    usuarios_repo.create_usuario(conn, ("admin", hash_password("1234"), "admin", 1))

    # 2. Stub conn_factory para usar SIEMPRE esta conexión
    def conn_ctx():
        class Ctx:
            def __enter__(self): return conn
            def __exit__(self, exc_type, exc, tb):
                conn.close()

        return Ctx()

    # 3. LoginController
    logged = {"user": None}
    login_controller = LoginController(
        login_fn=login,
        conn_factory=lambda: conn_ctx(),
        on_success=lambda u: logged.update(user=u)
    )

    ok = login_controller.login("admin", "1234")
    assert ok is True
    assert logged["user"]["usuario"] == "admin"

    # 4. DashboardController
    msgs = {"info": None, "error": None}
    dash_controller = DashboardController(
        conn_factory=lambda: conn_ctx(),
        on_info=lambda m: msgs.update(info=m),
        on_error=lambda m: msgs.update(error=m)
    )

    # Crear producto
    ok = dash_controller.crear_producto("perno", 10)
    assert ok is True
    assert msgs["info"] == "Producto creado correctamente"

    producto = productos_repo.get_producto(conn, 1)
    assert producto["stock"] == 10

    # Registrar venta
    ok = dash_controller.registrar_venta(logged["user"]["id_usuario"], 1, 2, 1.5)
    assert ok is True
    assert msgs["info"] == "Venta registrada correctamente"

    producto = productos_repo.get_producto(conn, 1)
    assert producto["stock"] == 8  # 10 - 2