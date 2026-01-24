# ui/productos_controller.py
from database.repositories import productos_repo
from utils.db import SafeConnection

class ProductosController:
    def __init__(self, conn_factory, on_info, on_error):
        self.conn_factory = conn_factory
        self.on_info = on_info
        self.on_error = on_error

    def crear(self, tipo, medida, largo, material, precio, stock, id_proveedor):
        try:
            with SafeConnection(lambda: self.conn_factory()) as conn:  # ✅
                productos_repo.create_producto(conn, (tipo, medida, largo, material, precio, stock, id_proveedor))
            self.on_info("Producto creado")
            return True
        except Exception as e:
            self.on_error(str(e))
            return False

    def editar(self, id_producto, **fields):
        if not fields:
            self.on_error("Sin cambios")
            return False
        with SafeConnection(lambda: self.conn_factory()) as conn:  # ✅
            ok = productos_repo.update_producto(conn, id_producto, fields)
        if not ok:
            self.on_error("Producto no encontrado")
            return False
        self.on_info("Producto actualizado")
        return True

    def eliminar(self, id_producto, borrado_logico=True):
        with SafeConnection(lambda: self.conn_factory()) as conn:  # ✅
            if borrado_logico:
                ok = productos_repo.update_producto(conn, id_producto, {"activo": 0})
            else:
                ok = productos_repo.delete_producto(conn, id_producto)
        if not ok:
            self.on_error("No se pudo eliminar")
            return False
        self.on_info("Producto eliminado")
        return True

    def listar(self, tipo=None):
        with SafeConnection(lambda: self.conn_factory()) as conn:  # ✅
            return productos_repo.list_productos(conn, tipo)

    def obtener(self, id_producto):
        with SafeConnection(lambda: self.conn_factory()) as conn:  # ✅
            return productos_repo.get_producto(conn, id_producto)