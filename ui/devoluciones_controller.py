# ui/devoluciones_controller.py
from database.repositories import devoluciones_repo, ventas_repo, productos_repo
from utils.db import SafeConnection

class DevolucionesController:
    def __init__(self, conn_factory, on_info, on_error):
        self.conn_factory = conn_factory
        self.on_info = on_info
        self.on_error = on_error

    def registrar(self, id_venta, id_producto, cantidad, id_usuario, observacion="", reinserta_stock=False):
        try:
            with SafeConnection(lambda: self.conn_factory()) as conn:
                devoluciones_repo.create_devolucion(
                    conn,
                    id_venta,
                    id_usuario,
                    observacion,
                    id_producto,
                    cantidad
                )
                if reinserta_stock:
                    productos_repo.sumar_stock(conn, id_producto, cantidad)

            self.on_info("Devolución registrada")
            return True
        except Exception as e:
            self.on_error(f"Error al registrar devolución: {e}")
            return False

    def listar(self):
        with SafeConnection(lambda: self.conn_factory()) as conn:
            return devoluciones_repo.list_devoluciones(conn)

    def detalle(self, id_devolucion):
        with SafeConnection(lambda: self.conn_factory()) as conn:
            return devoluciones_repo.list_detalle(conn, id_devolucion)

    def ventas_por_fecha(self, fecha):
        with SafeConnection(lambda: self.conn_factory()) as conn:
            return ventas_repo.list_ventas_por_fecha(conn, fecha)

    def listar_productos(self):
        with SafeConnection(lambda: self.conn_factory()) as conn:
            return productos_repo.list_productos(conn)