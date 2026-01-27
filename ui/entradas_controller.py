# ui/entradas_controller.py
from database.repositories import entradas_repo, proveedores_repo, productos_repo
from services.entradas_service import registrar_entrada
from utils.db import SafeConnection

class EntradasController:
    def __init__(self, conn_factory, on_info, on_error, on_productos_updated=None):
        self.conn_factory = conn_factory
        self.on_info = on_info
        self.on_error = on_error
        self.on_productos_updated = on_productos_updated

    def registrar(self, id_producto, cantidad, id_proveedor, id_usuario, observacion=""):
        try:
            with SafeConnection(lambda: self.conn_factory()) as conn:
                detalles = [{
                    "id_producto": id_producto,
                    "cantidad": cantidad,
                    "tipo_ingreso": "unidad",
                    "precio_compra": 0.0
                }]
                registrar_entrada(id_proveedor, id_usuario, observacion, detalles, conn)
            self.on_info("Entrada registrada")
            if self.on_productos_updated:
                self.on_productos_updated()   # 🔥 refrescar Productos en UI
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