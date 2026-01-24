import pytest
import sqlite3
from services.ventas_service import registrar_venta
from services.entradas_service import registrar_entrada
from services.devoluciones_service import registrar_devolucion
from database.repositories import productos_repo
from tests.fixtures import usuario_base, proveedor_base, producto_base

# --- Ventas ---
def test_venta_cantidad_cero(test_conn):
    id_usuario = usuario_base(test_conn)
    producto_base(test_conn, stock=10)
    detalles = [{"id_producto": 1, "cantidad": 0, "precio_unitario": 1.5}]
    id_venta = registrar_venta(id_usuario, detalles, conn=test_conn)
    producto = productos_repo.get_producto(test_conn, 1)
    assert producto["stock"] == 10  # stock no cambia

def test_venta_stock_exactamente_minimo(test_conn):
    id_usuario = usuario_base(test_conn)
    producto_base(test_conn, stock=5)
    detalles = [{"id_producto": 1, "cantidad": 5, "precio_unitario": 1.5}]
    id_venta = registrar_venta(id_usuario, detalles, conn=test_conn)
    producto = productos_repo.get_producto(test_conn, 1)
    assert producto["stock"] == 0  # se descuenta todo

# --- Entradas ---
def test_entrada_cantidad_cero(test_conn):
    id_usuario = usuario_base(test_conn)
    id_proveedor = proveedor_base(test_conn)
    producto_base(test_conn, stock=5)
    detalles = [{"id_producto": 1, "cantidad": 0, "precio_compra": 1.5}]
    id_entrada = registrar_entrada(id_proveedor, id_usuario, "compra inicial", detalles, conn=test_conn)
    producto = productos_repo.get_producto(test_conn, 1)
    assert producto["stock"] == 5  # stock no cambia

def test_entrada_precio_negativo(test_conn):
    id_usuario = usuario_base(test_conn)
    id_proveedor = proveedor_base(test_conn)
    producto_base(test_conn, stock=5)
    with pytest.raises(sqlite3.IntegrityError):
        registrar_entrada(id_proveedor, id_usuario, "compra inicial", [{"id_producto": 1, "cantidad": 5, "precio_compra": -1.0}], conn=test_conn)

# --- Devoluciones ---
def test_devolucion_mayor_stock(test_conn):
    id_usuario = usuario_base(test_conn)
    producto_base(test_conn, stock=2)
    # Crear venta
    from database.repositories import ventas_repo
    ventas_repo.create_venta(test_conn, ("2026-01-21", id_usuario, 3.0))
    # Devolver más de lo vendido (esto reintegra stock)
    detalles = [{"id_producto": 1, "cantidad": 5}]
    id_devolucion = registrar_devolucion(1, id_usuario, "cliente devolvió", detalles, conn=test_conn)
    producto = productos_repo.get_producto(test_conn, 1)
    assert producto["stock"] == 7  # stock inicial 2 + 5 devueltos

def test_devolucion_observacion_vacia(test_conn):
    id_usuario = usuario_base(test_conn)
    producto_base(test_conn, stock=5)
    from database.repositories import ventas_repo
    ventas_repo.create_venta(test_conn, ("2026-01-21", id_usuario, 7.5))
    detalles = [{"id_producto": 1, "cantidad": 2}]
    id_devolucion = registrar_devolucion(1, id_usuario, "", detalles, conn=test_conn)
    producto = productos_repo.get_producto(test_conn, 1)
    assert producto["stock"] == 7  # stock inicial 5 + 2 devueltos