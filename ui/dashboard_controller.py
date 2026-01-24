# ui/dashboard_controller.py
from database.repositories import productos_repo
from services.ventas_service import registrar_venta
from utils.db import SafeConnection

class DashboardController:
    def __init__(self, conn_factory, on_info, on_error):
        self.conn_factory = conn_factory
        self.on_info = on_info
        self.on_error = on_error

    def crear_producto(self, tipo, stock):
        if not tipo or not isinstance(stock, int) or stock < 0:
            self.on_error("Tipo y stock deben ser válidos")
            return False

        with SafeConnection(lambda: self.conn_factory()) as conn:  # ✅ factory → conexión real
            productos_repo.create_producto(
                conn, (tipo, "M8", "30mm", "acero", 1.5, stock, 2)
            )
        self.on_info("Producto creado correctamente")
        return True

    def registrar_venta(self, id_usuario, id_producto, cantidad, precio):
        if cantidad <= 0 or precio <= 0:
            self.on_error("Cantidad y precio deben ser positivos")
            return False

        detalles = [{"id_producto": id_producto, "cantidad": cantidad, "precio_unitario": precio}]
        try:
            with SafeConnection(lambda: self.conn_factory()) as conn:  # ✅
                registrar_venta(id_usuario, detalles, conn=conn)
            self.on_info("Venta registrada correctamente")
            return True
        except ValueError as e:
            self.on_error(str(e))
            return False