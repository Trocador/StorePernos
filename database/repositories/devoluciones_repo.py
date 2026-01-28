# database/repositories/devoluciones_repo.py
def create_devolucion(conn, id_venta, id_usuario, observacion, id_producto, cantidad):
    # Crear cabecera
    sql = "INSERT INTO devoluciones (id_venta, id_usuario, observacion) VALUES (?, ?, ?)"
    cur = conn.execute(sql, (id_venta, id_usuario, observacion))
    id_devolucion = cur.lastrowid

    # Crear detalle
    sql_det = """INSERT INTO devolucion_detalle (id_devolucion, id_producto, cantidad)
                 VALUES (?, ?, ?)"""
    conn.execute(sql_det, (id_devolucion, id_producto, cantidad))

    return id_devolucion


def list_devoluciones(conn):
    sql = """
    SELECT d.id_devolucion,
           d.id_venta,
           d.fecha,
           d.id_usuario,
           d.observacion
    FROM devoluciones d
    ORDER BY d.fecha DESC
    """
    return conn.execute(sql).fetchall()


def list_detalle(conn, id_devolucion):
    sql = """
    SELECT dd.id_detalle,
           dd.id_producto,   -- 🔥 añadir este campo
           (p.tipo || ' ' || p.medida || ' ' || IFNULL(p.largo,'')) AS producto,
           dd.cantidad
    FROM devolucion_detalle dd
    JOIN productos p ON dd.id_producto = p.id_producto
    WHERE dd.id_devolucion = ?
    """
    return conn.execute(sql, (id_devolucion,)).fetchall()