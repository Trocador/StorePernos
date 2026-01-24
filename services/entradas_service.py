# services/entradas_service.py

from database.connection import get_connection
from database.repositories import entradas_repo, productos_repo

def registrar_entrada(id_proveedor, id_usuario, observacion, detalles, conn):
    id_entrada = entradas_repo.create_entrada(conn, id_proveedor, id_usuario, observacion)

    for d in detalles:
        entradas_repo.create_entrada_detalle(
            conn,
            id_entrada,
            d["id_producto"],
            d["cantidad"],
            d.get("tipo_ingreso"),
            d.get("precio_compra"),
        )

        productos_repo.sumar_stock(conn, d["id_producto"], d["cantidad"])

    return id_entrada



def _registrar_entrada(c, id_proveedor, id_usuario, observacion, detalles):
    id_entrada = entradas_repo.create_entrada(c, (None, id_proveedor, id_usuario, observacion))

    for d in detalles:
        sql = """INSERT INTO entrada_detalle(id_entrada, id_producto, cantidad, precio_compra)
                 VALUES (?, ?, ?, ?)"""
        c.execute(sql, (id_entrada, d["id_producto"], d["cantidad"], d["precio_compra"]))

        producto = productos_repo.get_producto(c, d["id_producto"])
        nuevo_stock = producto["stock"] + d["cantidad"]
        productos_repo.update_stock(c, d["id_producto"], nuevo_stock)

    return id_entrada