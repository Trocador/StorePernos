# database/repositories/movimientos_repo.py

def get_movimientos_by_producto(conn, id_producto):
    sql = "SELECT * FROM movimientos_stock WHERE id_producto=? ORDER BY fecha DESC"
    return conn.execute(sql, (id_producto,)).fetchall()

def get_movimientos_by_fecha(conn, fecha_inicio, fecha_fin):
    sql = "SELECT * FROM movimientos_stock WHERE fecha BETWEEN ? AND ? ORDER BY fecha DESC"
    return conn.execute(sql, (fecha_inicio, fecha_fin)).fetchall()