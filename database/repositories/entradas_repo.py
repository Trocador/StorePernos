# database/repositories/entradas_repo.py
def create_entrada(conn, id_proveedor, id_usuario, observacion, id_producto, cantidad):
    # Crear cabecera
    sql = "INSERT INTO entradas (id_proveedor, id_usuario, observacion) VALUES (?, ?, ?)"
    cur = conn.execute(sql, (id_proveedor, id_usuario, observacion))
    id_entrada = cur.lastrowid

    # Crear detalle
    sql_det = """INSERT INTO entrada_detalle (id_entrada, id_producto, cantidad, tipo_ingreso, precio_compra)
                 VALUES (?, ?, ?, ?, ?)"""
    conn.execute(sql_det, (id_entrada, id_producto, cantidad, "unidad", 0.0))

    return id_entrada

def list_entradas(conn):
    sql = """
    SELECT e.id_entrada,
           e.fecha,
           pr.nombre AS proveedor,
           e.id_usuario,
           e.observacion,
           (p.tipo || ' ' || p.medida || ' ' || IFNULL(p.largo,'')) AS producto,
           ed.cantidad
    FROM entradas e
    JOIN proveedores pr ON e.id_proveedor = pr.id_proveedor
    JOIN entrada_detalle ed ON e.id_entrada = ed.id_entrada
    JOIN productos p ON ed.id_producto = p.id_producto
    ORDER BY e.fecha DESC
    """
    return conn.execute(sql).fetchall()


def list_detalle(conn, id_entrada):
    sql = """
    SELECT ed.id_detalle,
           (p.tipo || ' ' || p.medida || ' ' || IFNULL(p.largo,'')) AS producto,
           ed.cantidad,
           ed.tipo_ingreso,
           ed.precio_compra
    FROM entrada_detalle ed
    JOIN productos p ON ed.id_producto = p.id_producto
    WHERE ed.id_entrada = ?
    """
    return conn.execute(sql, (id_entrada,)).fetchall()
