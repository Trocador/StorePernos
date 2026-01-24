import sqlite3
from ui.login_controller import LoginController
from ui.productos_controller import ProductosController
from ui.ventas_controller import VentasController
from ui.entradas_controller import EntradasController
from ui.devoluciones_controller import DevolucionesController
from database.repositories import usuarios_repo, productos_repo, proveedores_repo
from utils.security import hash_password
from services.auth_service import login

def conn_factory_memory(schema_path="database/schema.sql"):
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    return conn

def test_e2e_flow():
    conn = conn_factory_memory()
    usuarios_repo.create_usuario(conn, ("admin", hash_password("1234"), "admin", 1))
    proveedores_repo.create_proveedor(conn, ("Proveedor Test", "12345678"))

    def ctx():
        class Ctx:
            def __enter__(self): return conn
            def __exit__(self, exc_type, exc, tb): 
                pass  # ✅ no cerramos en tests
        return Ctx()

    msgs = {"info": [], "error": []}
    on_info = lambda m: msgs["info"].append(m)
    on_error = lambda m: msgs["error"].append(m)

    # Login
    logged = {"user": None}
    LoginController(login, lambda: ctx(), lambda u: logged.update(user=u)).login("admin", "1234")
    assert logged["user"]

    # Productos
    pc = ProductosController(lambda: ctx(), on_info, on_error)
    assert pc.crear("perno", "M8", "30mm", "acero", 1.5, 10, 1)
    with ctx() as conn2:
        prod = productos_repo.get_producto(conn2, 1)
    assert prod["stock"] == 10

    # Entradas
    ec = EntradasController(lambda: ctx(), on_info, on_error)
    assert ec.registrar(1, 5, 1)
    with ctx() as conn2:
        prod = productos_repo.get_producto(conn2, 1)
    assert prod["stock"] == 15

    # Ventas
    vc = VentasController(lambda: ctx(), on_info, on_error)
    assert vc.registrar(
        logged["user"]["id_usuario"], 
        [{"id_producto": 1, "cantidad": 3, "precio_unitario": 2.0}]
    )
    with ctx() as conn2:
        prod = productos_repo.get_producto(conn2, 1)
    assert prod["stock"] == 12

    # Devoluciones
    dc = DevolucionesController(lambda: ctx(), on_info, on_error)
    assert dc.registrar(1, 1, 2, "Cliente devolvió", logged["user"]["id_usuario"])
    with ctx() as conn2:
        prod = productos_repo.get_producto(conn2, 1)
    assert prod["stock"] == 14
