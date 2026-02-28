# database/repositories/ventas_repo.py

def create_venta(conn, venta):
    sql = """INSERT INTO ventas(fecha, id_usuario, total)
             VALUES (?, ?, ?)"""
    cur = conn.execute(sql, venta)
    return cur.lastrowid  # devolver id de la venta


def get_venta(conn, id_venta):
    sql = """
    SELECT v.id_venta, v.fecha, v.total, u.usuario
    FROM ventas v
    JOIN usuarios u ON v.id_usuario = u.id_usuario
    WHERE v.id_venta=?
    """
    return conn.execute(sql, (id_venta,)).fetchone()


def get_ventas_by_fecha(conn, fecha_inicio, fecha_fin):
    sql = """
    SELECT v.id_venta, v.fecha, v.total, u.usuario
    FROM ventas v
    JOIN usuarios u ON v.id_usuario = u.id_usuario
    WHERE v.fecha BETWEEN ? AND ?
    ORDER BY v.fecha DESC
    """
    return conn.execute(sql, (fecha_inicio, fecha_fin)).fetchall()


def list_ventas(conn, fecha_desde=None, fecha_hasta=None):
    sql = """
    SELECT v.id_venta, u.usuario, v.fecha, v.total
    FROM ventas v
    JOIN usuarios u ON v.id_usuario = u.id_usuario
    """
    params = []
    if fecha_desde and fecha_hasta:
        sql += " WHERE v.fecha BETWEEN ? AND ?"
        params = [fecha_desde, fecha_hasta]

    sql += " ORDER BY v.fecha DESC"
    return conn.execute(sql, params).fetchall()


def get_venta_detalle(conn, id_venta):
    sql = """SELECT vd.id_detalle,
                    vd.id_producto,
                    (p.tipo || ' ' || p.medida || ' ' || IFNULL(p.largo,'')) AS producto,
                    vd.cantidad,
                    vd.tipo_venta,
                    vd.precio_unitario,
                    vd.subtotal
             FROM venta_detalle vd
             JOIN productos p ON p.id_producto = vd.id_producto
             WHERE vd.id_venta = ?"""
    return conn.execute(sql, (id_venta,)).fetchall()


def list_ventas_por_fecha(conn, fecha):
    sql = """
    SELECT v.id_venta, u.usuario, v.fecha, v.total
    FROM ventas v
    JOIN usuarios u ON v.id_usuario = u.id_usuario
    WHERE DATE(v.fecha) = DATE(?)
    ORDER BY v.fecha DESC
    """
    return conn.execute(sql, (fecha,)).fetchall()


def get_total_ventas_rango(conn, fecha_inicio, fecha_fin):
    sql = """
        SELECT IFNULL(SUM(total), 0) as total_vendido
        FROM ventas
        WHERE DATE(fecha) BETWEEN DATE(?) AND DATE(?)
    """
    row = conn.execute(sql, (fecha_inicio, fecha_fin)).fetchone()
    return row["total_vendido"] if row else 0


def list_ventas_semana(conn, fecha):
    sql = """
    SELECT v.id_venta, u.usuario, v.fecha, v.total
    FROM ventas v
    JOIN usuarios u ON v.id_usuario = u.id_usuario
    WHERE strftime('%W', v.fecha) = strftime('%W', ?)
      AND strftime('%Y', v.fecha) = strftime('%Y', ?)
    ORDER BY v.fecha DESC
    """
    return conn.execute(sql, (fecha, fecha)).fetchall()