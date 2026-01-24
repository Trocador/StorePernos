# tests/test_ventas.py
from services.ventas_service import registrar_venta
from database.repositories import productos_repo
from tests.fixtures import usuario_base, producto_base

def test_registrar_venta_disminuye_stock(test_conn):
    id_usuario = usuario_base(test_conn)
    producto_base(test_conn, stock=10)

    detalles = [{"id_producto": 1, "cantidad": 5, "precio_unitario": 1.5}]
    id_venta = registrar_venta(id_usuario, detalles, conn=test_conn)

    producto = productos_repo.get_producto(test_conn, 1)
    assert int(producto["stock"]) == 5