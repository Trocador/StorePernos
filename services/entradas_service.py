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