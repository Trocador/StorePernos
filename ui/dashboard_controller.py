# ui/dashboard_controller.py
import datetime
from database.repositories import productos_repo, ventas_repo
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

        with SafeConnection(lambda: self.conn_factory()) as conn:  # factory → conexión real
            productos_repo.create_producto(
                conn, (tipo, "M8", "30mm", "acero", 1.5, stock, 2)
            )
        self.on_info("Producto creado correctamente")
        return True

    def registrar_venta(self, id_usuario, id_producto, cantidad, precio):
        if cantidad <= 0 or precio <= 0:
            self.on_error("Cantidad y precio deben ser positivos")
            return False

        detalles = [{
            "id_producto": id_producto,
            "cantidad": cantidad,
            "precio_unitario": precio,
            "subtotal": cantidad * precio,   # calcular subtotal
            "tipo_venta": "unidad"           # o "kilo", según tu lógica
        }]
        try:
            with SafeConnection(lambda: self.conn_factory()) as conn:  #
                registrar_venta(id_usuario, detalles, conn=conn)
            self.on_info("Venta registrada correctamente")
            return True
        except ValueError as e:
            self.on_error(str(e))
            return False
    
    def obtener_kpis(self):
        """Devuelve métricas clave para el Dashboard"""
        try:
            with SafeConnection(lambda: self.conn_factory()) as conn:
                # 🔹 Ventas del día (suma de total)
                hoy = datetime.date.today().strftime("%Y-%m-%d")
                ventas_hoy = ventas_repo.get_total_ventas_rango(conn, hoy, hoy)

                # 🔹 Stock bajo (ejemplo: productos con stock < stock_minimo)
                cur = conn.execute("SELECT COUNT(*) as cnt FROM productos WHERE stock < stock_minimo AND activo=1")
                stock_bajo = cur.fetchone()["cnt"]

                # 🔹 Productos totales
                cur = conn.execute("SELECT COUNT(*) as cnt FROM productos WHERE activo=1")
                productos_totales = cur.fetchone()["cnt"]

                # 🔹 Promociones activas (si tienes tabla promociones, aquí se consulta)
                try:
                    cur = conn.execute("SELECT COUNT(*) as cnt FROM promociones WHERE activa=1")
                    promociones_activas = cur.fetchone()["cnt"]
                except Exception:
                    promociones_activas = 0

            return {
                "ventas_hoy": ventas_hoy,
                "stock_bajo": stock_bajo,
                "productos_totales": productos_totales,
                "promociones_activas": promociones_activas
            }
        except Exception as e:
            self.on_error(f"Error al obtener KPIs: {e}")
            return {
                "ventas_hoy": 0,
                "stock_bajo": 0,
                "productos_totales": 0,
                "promociones_activas": 0
            }