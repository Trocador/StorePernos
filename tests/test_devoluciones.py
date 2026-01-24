# tests/test_devoluciones.py
from services.devoluciones_service import registrar_devolucion
from database.repositories import ventas_repo, productos_repo
from tests.fixtures import usuario_base, producto_base

def test_registrar_devolucion_reintegra_stock(test_conn):
    id_usuario = usuario_base(test_conn)
    producto_base(test_conn, stock=10)

    # Crear venta ligada al usuario
    ventas_repo.create_venta(test_conn, ("2026-01-21", id_usuario, 30.0))

    detalles = [{"id_producto": 1, "cantidad": 2}]
    id_devolucion = registrar_devolucion(1, id_usuario, "cliente devolvió", detalles, conn=test_conn)

    producto = productos_repo.get_producto(test_conn, 1)
    assert int(producto["stock"]) == 12  # stock inicial 10 + 2 devueltos