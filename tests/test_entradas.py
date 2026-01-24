# tests/test_entradas.py
from services.entradas_service import registrar_entrada
from database.repositories import productos_repo
from tests.fixtures import usuario_base, proveedor_base, producto_base

def test_registrar_entrada_aumenta_stock(test_conn):
    id_usuario = usuario_base(test_conn)
    id_proveedor = proveedor_base(test_conn)
    producto_base(test_conn, stock=0)

    detalles = [{"id_producto": 1, "cantidad": 10, "precio_compra": 1.5}]
    id_entrada = registrar_entrada(id_proveedor, id_usuario, "compra inicial", detalles, conn=test_conn)

    producto = productos_repo.get_producto(test_conn, 1)
    assert int(producto["stock"]) == 10