from database.repositories import proveedores_repo
from utils.db import SafeConnection

class ProveedoresController:
    def __init__(self, conn_factory, on_info, on_error):
        self.conn_factory = conn_factory
        self.on_info = on_info
        self.on_error = on_error

    def crear(self, nombre, contacto=""):
        if not nombre:
            self.on_error("Nombre requerido")
            return False
        with SafeConnection(lambda: self.conn_factory()) as conn:
            proveedores_repo.create_proveedor(conn, (nombre, contacto))
        self.on_info("Proveedor creado")
        return True

    def listar(self):
        with SafeConnection(lambda: self.conn_factory()) as conn:
            return proveedores_repo.list_proveedores(conn)

    def editar(self, id_proveedor, **fields):
        if not fields:
            self.on_error("Sin cambios")
            return False
        with SafeConnection(lambda: self.conn_factory()) as conn:
            ok = proveedores_repo.update_proveedor(conn, id_proveedor, fields)
        if not ok:
            self.on_error("Proveedor no encontrado")
            return False
        self.on_info("Proveedor actualizado")
        return True

    def eliminar(self, id_proveedor):
        with SafeConnection(lambda: self.conn_factory()) as conn:
            ok = proveedores_repo.delete_proveedor(conn, id_proveedor)
        if not ok:
            self.on_error("No se pudo eliminar")
            return False
        self.on_info("Proveedor eliminado")
        return True