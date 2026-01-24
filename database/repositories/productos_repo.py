# database/repositories/productos_repo.py
def create_producto(conn, producto):
    sql = """INSERT INTO productos(tipo, medida, largo, material, precio_unidad, stock, stock_minimo)
             VALUES (?, ?, ?, ?, ?, ?, ?)"""
    conn.execute(sql, producto)

def get_all(conn):
    rows = conn.execute("SELECT id_producto, tipo, medida, largo FROM productos").fetchall()
    return [(row["id_producto"], f"{row['tipo']} {row['medida']} {row['largo'] or ''}") for row in rows]

def update_producto(conn, id_producto, fields: dict):
    if not fields: return False
    cols = ", ".join([f"{k} = ?" for k in fields.keys()])
    sql = f"UPDATE productos SET {cols} WHERE id_producto = ?"
    params = list(fields.values()) + [id_producto]
    cur = conn.execute(sql, params)
    return cur.rowcount > 0

def update_stock(conn, id_producto, nuevo_stock):
    sql = "UPDATE productos SET stock = ? WHERE id_producto = ?"
    conn.execute(sql, (nuevo_stock, id_producto))

def deactivate_producto(conn, id_producto):
    sql = "UPDATE productos SET activo=0 WHERE id_producto=?"
    conn.execute(sql, (id_producto,))

def list_productos(conn, tipo=None):
    if tipo:
        return conn.execute("SELECT * FROM productos WHERE tipo = ? AND activo = 1", (tipo,)).fetchall()
    return conn.execute("SELECT * FROM productos WHERE activo = 1").fetchall()

def sumar_stock(conn, id_producto, cantidad):
    sql = "UPDATE productos SET stock = stock + ? WHERE id_producto = ?"
    conn.execute(sql, (cantidad, id_producto))

def restar_stock(conn, id_producto, cantidad):
    sql = "UPDATE productos SET stock = stock - ? WHERE id_producto = ?"
    conn.execute(sql, (cantidad, id_producto))
