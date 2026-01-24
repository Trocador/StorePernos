# ui/entradas_controller.py
from database.repositories import entradas_repo, proveedores_repo, productos_repo
from utils.db import SafeConnection

class EntradasController:
    def __init__(self, conn_factory, on_info, on_error):
        self.conn_factory = conn_factory
        self.on_info = on_info
        self.on_error = on_error

    def registrar(self, id_producto, cantidad, id_proveedor, id_usuario, observacion=""):
        try:
            with SafeConnection(lambda: self.conn_factory()) as conn:
                entradas_repo.create_entrada(conn, id_proveedor, id_usuario, observacion, id_producto, cantidad)
            self.on_info("Entrada registrada")
            return True
        except Exception as e:
            self.on_error(f"Error al registrar entrada: {e}")
            return False

    def listar(self):
        with SafeConnection(lambda: self.conn_factory()) as conn:
            return entradas_repo.list_entradas(conn)

    def detalle(self, id_entrada):
        with SafeConnection(lambda: self.conn_factory()) as conn:
            return entradas_repo.list_detalle(conn, id_entrada)
    def obtener_proveedores(self):
        with self.conn_factory() as conn:
            return proveedores_repo.get_all(conn)

    def obtener_productos(self):
        with self.conn_factory() as conn:
            return productos_repo.get_all(conn)