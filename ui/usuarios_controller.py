# ui/usuarios_controller.py
from database.repositories import usuarios_repo
from utils.security import hash_password
from utils.db import SafeConnection

class UsuariosController:
    def __init__(self, conn_factory, on_info, on_error):
        self.conn_factory = conn_factory
        self.on_info = on_info
        self.on_error = on_error

    def crear_usuario(self, usuario, password, rol):
        if not usuario or not password or not rol:
            self.on_error("Todos los campos son obligatorios")
            return False

        try:
            with SafeConnection(lambda: self.conn_factory()) as conn:  # ✅
                usuarios_repo.create_usuario(
                    conn,
                    (usuario, hash_password(password), rol, 1)  # activo=1 por defecto
                )
            self.on_info("Usuario creado correctamente")
            return True
        except Exception as e:
            self.on_error(f"Error al crear usuario: {e}")
            return False

    def listar(self):
        with SafeConnection(lambda: self.conn_factory()) as conn:  # ✅
            return usuarios_repo.list_usuarios(conn)