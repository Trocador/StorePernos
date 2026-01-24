# database/repositories/usuarios_repo.py

def create_usuario(conn, usuario):
    sql = """INSERT INTO usuarios(usuario, password_hash, rol, activo)
             VALUES (?, ?, ?, ?)"""
    cur = conn.execute(sql, usuario)
    return cur.lastrowid


def get_usuario(conn, usuario):
    sql = """
    SELECT id_usuario, usuario, password_hash, rol, activo
    FROM usuarios
    WHERE usuario=?
    """
    return conn.execute(sql, (usuario,)).fetchone()

def update_usuario(conn, usuario):
    sql = """UPDATE usuarios
             SET password_hash=?, rol=?, activo=?
             WHERE id_usuario=?"""
    conn.execute(sql, usuario)

def deactivate_usuario(conn, id_usuario):
    sql = "UPDATE usuarios SET activo=0 WHERE id_usuario=?"
    conn.execute(sql, (id_usuario,))

def list_usuarios(conn):
    sql = "SELECT id_usuario, usuario, rol, activo FROM usuarios"
    return conn.execute(sql).fetchall()
