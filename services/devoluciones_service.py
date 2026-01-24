# services/devoluciones_service.py

from database.connection import get_connection
from database.repositories import devoluciones_repo, productos_repo

def registrar_devolucion(id_venta, id_usuario, observacion, detalles, conn):
    id_dev = devoluciones_repo.create_devolucion(conn, id_venta, id_usuario, observacion)

    for d in detalles:
        devoluciones_repo.create_devolucion_detalle(
            conn,
            id_dev,
            d["id_producto"],
            d["cantidad"]
        )

        productos_repo.sumar_stock(conn, d["id_producto"], d["cantidad"])

    return id_dev

def _registrar_devolucion(c, id_venta, id_usuario, observacion, detalles):
    id_devolucion = devoluciones_repo.create_devolucion(
        c, (id_venta, id_usuario, observacion)
    )

    for d in detalles:
        sql = """INSERT INTO devolucion_detalle(id_devolucion, id_producto, cantidad)
                 VALUES (?, ?, ?)"""
        c.execute(sql, (id_devolucion, d["id_producto"], d["cantidad"]))

        # Reintegrar stock
        producto = productos_repo.get_producto(c, d["id_producto"])
        nuevo_stock = producto["stock"] + d["cantidad"]
        productos_repo.update_stock(c, d["id_producto"], nuevo_stock)

        # Registrar movimiento
        c.execute("""INSERT INTO movimientos_stock(id_producto, tipo, cantidad, fecha, referencia, id_usuario)
                     VALUES (?, 'devolucion', ?, CURRENT_TIMESTAMP, ?, ?)""",
                  (d["id_producto"], d["cantidad"], f"devolucion:{id_devolucion}", id_usuario))

    return id_devolucion