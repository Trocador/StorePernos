# services/ventas_service.py

from datetime import datetime
from database.connection import get_connection
from database.repositories import ventas_repo, productos_repo

def registrar_venta(id_usuario, detalles, conn=None):
    if conn:
        return _registrar_venta(conn, id_usuario, detalles)
    else:
        with get_connection() as c:
            return _registrar_venta(c, id_usuario, detalles)


def _registrar_venta(conn, id_usuario, detalles):
    total = sum(d["subtotal"] for d in detalles)
    id_venta = ventas_repo.create_venta(conn, (datetime.now(), id_usuario, total))

    for d in detalles:
        # insertar detalle
        sql = """INSERT INTO venta_detalle(id_venta, id_producto, cantidad, tipo_venta, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)"""
        conn.execute(sql, (id_venta, d["id_producto"], d["cantidad"], d["tipo_venta"], d["precio_unitario"], d["subtotal"]))

        # 🔥 validar stock antes de actualizar
        producto = productos_repo.get_producto(conn, d["id_producto"])
        if producto["stock"] < d["cantidad"]:
            raise ValueError(f"Stock insuficiente para producto {producto['id_producto']}")

        # actualizar stock
        conn.execute("UPDATE productos SET stock = stock - ? WHERE id_producto = ?", (d["cantidad"], d["id_producto"]))

    conn.commit()
    return id_venta