# database/repositories/proveedores_repo.py

def create_proveedor(conn, proveedor):
    """
    Inserta un proveedor en la tabla proveedores.
    proveedor = (nombre, contacto)
    """
    sql = """INSERT INTO proveedores(nombre, contacto)
             VALUES (?, ?)"""
    cur = conn.execute(sql, proveedor)
    return cur.lastrowid

def get_all(conn):
    rows = conn.execute("SELECT id_proveedor, nombre FROM proveedores").fetchall()
    return [(row["id_proveedor"], row["nombre"]) for row in rows]

def list_proveedores(conn, activo=1):
    """
    Devuelve todos los proveedores.
    Si activo=1, solo los activos; si activo=None, todos.
    """
    if activo is None:
        sql = "SELECT * FROM proveedores"
        return conn.execute(sql).fetchall()
    else:
        sql = "SELECT * FROM proveedores WHERE activo = ?"
        return conn.execute(sql, (activo,)).fetchall()

def update_proveedor(conn, id_proveedor, fields):
    """
    Actualiza los campos de un proveedor.
    fields es un diccionario con los campos a actualizar.
    """
    set_clause = ", ".join([f"{key}=?" for key in fields.keys()])
    sql = f"UPDATE proveedores SET {set_clause} WHERE id_proveedor=?"
    params = list(fields.values()) + [id_proveedor]
    cur = conn.execute(sql, params)
    return cur.rowcount > 0

def desactivate_proveedor(conn, id_proveedor):
    sql = "UPDATE proveedores SET activo=0 WHERE id_proveedor=?"
    cur = conn.execute(sql, (id_proveedor,))
    return cur.rowcount > 0

def activate_proveedor(conn, id_proveedor):
    sql = "UPDATE proveedores SET activo=1 WHERE id_proveedor=?"
    cur = conn.execute(sql, (id_proveedor,))
    return cur.rowcount > 0