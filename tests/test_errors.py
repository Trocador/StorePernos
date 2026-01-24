import pytest
import sqlite3
from services.ventas_service import registrar_venta
from services.entradas_service import registrar_entrada
from services.devoluciones_service import registrar_devolucion
from database.repositories import usuarios_repo
from tests.fixtures import usuario_base, proveedor_base, producto_base

# --- Ventas ---
def test_venta_producto_inexistente(test_conn):
    id_usuario = usuario_base(test_conn)
    with pytest.raises(ValueError, match="Producto no encontrado"):
        registrar_venta(id_usuario, [{"id_producto": 99, "cantidad": 1, "precio_unitario": 1.0}], conn=test_conn)

def test_venta_stock_insuficiente(test_conn):
    id_usuario = usuario_base(test_conn)
    producto_base(test_conn, stock=2)
    with pytest.raises(ValueError, match="Stock insuficiente"):
        registrar_venta(id_usuario, [{"id_producto": 1, "cantidad": 5, "precio_unitario": 1.5}], conn=test_conn)

# --- Entradas ---
def test_entrada_proveedor_inexistente(test_conn):
    id_usuario = usuario_base(test_conn)
    producto_base(test_conn)
    with pytest.raises(sqlite3.IntegrityError):
        registrar_entrada(99, id_usuario, "compra", [{"id_producto": 1, "cantidad": 5, "precio_compra": 1.0}], conn=test_conn)

# --- Devoluciones ---
def test_devolucion_venta_inexistente(test_conn):
    id_usuario = usuario_base(test_conn)
    producto_base(test_conn)
    with pytest.raises(sqlite3.IntegrityError):
        registrar_devolucion(99, id_usuario, "cliente devolvió", [{"id_producto": 1, "cantidad": 1}], conn=test_conn)

# --- Usuarios ---
def test_usuario_duplicado(test_conn):
    usuario_base(test_conn)
    with pytest.raises(sqlite3.IntegrityError):
        usuario_base(test_conn)  # mismo usuario otra vez