# services/ventas_service.py

from database.connection import get_connection
from database.repositories import ventas_repo, productos_repo

def registrar_venta(id_usuario, detalles, conn=None):
    if conn:
        return _registrar_venta(conn, id_usuario, detalles)
    else:
        with get_connection() as c:
            return _registrar_venta(c, id_usuario, detalles)


def _registrar_venta(c, id_usuario, detalles):
    total = 0
    for d in detalles:
        producto = productos_repo.get_producto(c, d["id_producto"])
        if not producto:
            raise ValueError("Producto no encontrado")
        if producto["stock"] < d["cantidad"]:
            raise ValueError("Stock insuficiente")

        d["subtotal"] = d["cantidad"] * d["precio_unitario"]
        total += d["subtotal"]

    id_venta = ventas_repo.create_venta(c, ("2026-01-21", id_usuario, total))

    for d in detalles:
        sql = """INSERT INTO venta_detalle(id_venta, id_producto, cantidad, tipo_venta, precio_unitario, subtotal)
                 VALUES (?, ?, ?, ?, ?, ?)"""
        c.execute(sql, (id_venta, d["id_producto"], d["cantidad"], "unidad", d["precio_unitario"], d["subtotal"]))

        producto = productos_repo.get_producto(c, d["id_producto"])
        nuevo_stock = producto["stock"] - d["cantidad"]
        productos_repo.update_stock(c, d["id_producto"], nuevo_stock)

        c.execute("""INSERT INTO movimientos_stock(id_producto, tipo, cantidad, fecha, referencia, id_usuario)
                     VALUES (?, 'venta', ?, CURRENT_TIMESTAMP, ?, ?)""",
                  (d["id_producto"], d["cantidad"], f"venta:{id_venta}", id_usuario))

    return id_venta