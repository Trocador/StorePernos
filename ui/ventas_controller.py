# ui/ventas_controller.py
from database.repositories import productos_repo, ventas_repo
from services.ventas_service import registrar_venta
from utils.db import SafeConnection

class VentasController:
    def __init__(self, conn_factory, on_info, on_error):
        self.conn_factory = conn_factory
        self.on_info = on_info
        self.on_error = on_error

    def registrar(self, id_usuario, items):
        # items: [{"id_producto": int, "cantidad": int, "precio_unitario": float}, ...]
        if not items:
            self.on_error("Venta vacía")
            return False
        for it in items:
            if it["cantidad"] <= 0 or it["precio_unitario"] <= 0:
                self.on_error("Cantidad y precio > 0")
                return False
        try:
            with SafeConnection(lambda: self.conn_factory()) as conn:  # ✅
                registrar_venta(id_usuario, items, conn=conn)
            self.on_info("Venta registrada")
            return True
        except ValueError as e:
            self.on_error(str(e))
            return False

    def listar(self, fecha_desde=None, fecha_hasta=None):
        with SafeConnection(lambda: self.conn_factory()) as conn:  # ✅
            return ventas_repo.list_ventas(conn, fecha_desde, fecha_hasta)

    def detalle(self, id_venta):
        with SafeConnection(lambda: self.conn_factory()) as conn:  # ✅
            return ventas_repo.get_venta_detalle(conn, id_venta)