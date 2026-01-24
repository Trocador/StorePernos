# tests/fixtures.py

from database.repositories import usuarios_repo, proveedores_repo, productos_repo
from utils.security import hash_password

def usuario_base(conn):
    usuarios_repo.create_usuario(conn, ("admin", hash_password("1234"), "admin", 1))
    return 1

def proveedor_base(conn):
    proveedores_repo.create_proveedor(conn, ("Proveedor Test", "123456"))
    return 1

def producto_base(conn, tipo="perno", medida="M8", largo="30mm", material="acero", precio=1.5, stock=10, stock_minimo=2):
    productos_repo.create_producto(conn, (tipo, medida, largo, material, precio, stock, stock_minimo))
    return 1