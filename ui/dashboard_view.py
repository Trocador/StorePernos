# ui/dashboard_view.py
from PIL import Image, ImageTk
import tkinter as tk
import ttkbootstrap as tb
from ui.productos_view import ProductosView
from ui.ventas_view import VentasView
from ui.entradas_view import EntradasView
from ui.devoluciones_view import DevolucionesView
from ui.usuarios_view import UsuariosView
from ui.usuarios_controller import UsuariosController
from ui.entradas_controller import EntradasController
from ui.devoluciones_controller import DevolucionesController
from ui.productos_controller import ProductosController
from ui.ventas_controller import VentasController
from ui.proveedores_controller import ProveedoresController
from ui.proveedores_view import ProveedoresView
from utils import backup
from utils.db import SafeConnection
from utils.backup import create_backup, restore_backup
from database.repositories import proveedores_repo, productos_repo

class DashboardView(tb.Frame):
    def __init__(self, master, controller, user, on_logout):
        super().__init__(master)
        self.controller = controller
        self.user = user
        self.on_logout = on_logout
        self._build()

    def _build(self):
        # --- Barra superior con botón de logout ---
        top_bar = tk.Frame(self)
        top_bar.pack(fill="x")

        tk.Button(top_bar, text="Crear Backup", command=self._crear_backup).pack(side="right", padx=10)
        tk.Button(top_bar, text="Restaurar Backup", command=self._restaurar_backup).pack(side="right", padx=10)

        tk.Label(top_bar, text=f"Usuario: {self.user['id_usuario']} ({self.user['rol']})").pack(side="left", padx=10)
        tk.Button(top_bar, text="Cerrar sesión", command=self._logout).pack(side="right", padx=10)

        # --- Contenedor principal ---
        self.container = tb.Frame(self)
        self.container.pack(fill="both", expand=True)

        # --- Menú lateral ---
        self.sidebar = tb.Frame(self.container, width=220)
        self.sidebar.pack(side="left", fill="y")

        # Cargar íconos PNG
        self.icon_productos = ImageTk.PhotoImage(Image.open("icons/caja.png").resize((20,20)))
        self.icon_ventas = ImageTk.PhotoImage(Image.open("icons/carrito-de-compras.png").resize((20,20)))
        self.icon_devoluciones = ImageTk.PhotoImage(Image.open("icons/devolucion-de-dinero.png").resize((20,20)))
        self.icon_proveedores = ImageTk.PhotoImage(Image.open("icons/proveedor.png").resize((20,20)))
        self.icon_entradas = ImageTk.PhotoImage(Image.open("icons/caja-entrada.png").resize((20,20)))
        self.icon_usuarios = ImageTk.PhotoImage(Image.open("icons/agregar-usuario.png").resize((20,20)))

        # Botones del menú lateral (conexión con pestañas)
        self.btn_productos = tb.Button(
            self.sidebar, text="Productos", image=self.icon_productos,
            compound="left", bootstyle="secondary-outline",
            command=lambda: self._select_tab("Productos")
        )
        self.btn_productos.pack(fill="x", pady=5, padx=10)

        self.btn_ventas = tb.Button(
            self.sidebar, text="Ventas", image=self.icon_ventas,
            compound="left", bootstyle="secondary-outline",
            command=lambda: self._select_tab("Ventas")
        )
        self.btn_ventas.pack(fill="x", pady=5, padx=10)

        self.btn_devoluciones = tb.Button(
            self.sidebar, text="Devoluciones", image=self.icon_devoluciones,
            compound="left", bootstyle="secondary-outline",
            command=lambda: self._select_tab("Devoluciones")
        )
        self.btn_devoluciones.pack(fill="x", pady=5, padx=10)

        if self.user["rol"] == "admin":
            self.btn_proveedores = tb.Button(
                self.sidebar, text="Proveedores", image=self.icon_proveedores,
                compound="left", bootstyle="secondary-outline",
                command=lambda: self._select_tab("Proveedores")
            )
            self.btn_proveedores.pack(fill="x", pady=5, padx=10)

            self.btn_entradas = tb.Button(
                self.sidebar, text="Entradas", image=self.icon_entradas,
                compound="left", bootstyle="secondary-outline",
                command=lambda: self._select_tab("Entradas")
            )
            self.btn_entradas.pack(fill="x", pady=5, padx=10)

            self.btn_usuarios = tb.Button(
                self.sidebar, text="Usuarios", image=self.icon_usuarios,
                compound="left", bootstyle="secondary-outline",
                command=lambda: self._select_tab("Usuarios")
            )
            self.btn_usuarios.pack(fill="x", pady=5, padx=10)

        # --- Área de contenido ---
        self.content = tb.Frame(self.container)
        self.content.pack(side="right", fill="both", expand=True)
        
        # --- Tarjetas KPI ---
        self.kpi_frame = tb.Frame(self.content)
        self.kpi_frame.pack(fill="x", pady=10)

        kpis = self.controller.obtener_kpis()

        # Ventas del día
        card_ventas = tb.Frame(self.kpi_frame, bootstyle="success", padding=15)
        card_ventas.pack(side="left", padx=10)
        tb.Label(card_ventas, text="Ventas Hoy", font=("Segoe UI", 10)).pack()
        tb.Label(card_ventas, text=f"Bs {kpis['ventas_hoy']}", font=("Segoe UI", 18, "bold")).pack()

        # Stock bajo
        card_stock = tb.Frame(self.kpi_frame, bootstyle="danger", padding=15)
        card_stock.pack(side="left", padx=10)
        tb.Label(card_stock, text="Stock Bajo", font=("Segoe UI", 10)).pack()
        tb.Label(card_stock, text=f"{kpis['stock_bajo']} productos", font=("Segoe UI", 18, "bold")).pack()

        # Productos totales
        card_productos = tb.Frame(self.kpi_frame, bootstyle="info", padding=15)
        card_productos.pack(side="left", padx=10)
        tb.Label(card_productos, text="Productos Totales", font=("Segoe UI", 10)).pack()
        tb.Label(card_productos, text=f"{kpis['productos_totales']}", font=("Segoe UI", 18, "bold")).pack()

        # Promociones activas
        card_promos = tb.Frame(self.kpi_frame, bootstyle="warning", padding=15)
        card_promos.pack(side="left", padx=10)
        tb.Label(card_promos, text="Promociones Activas", font=("Segoe UI", 10)).pack()
        tb.Label(card_promos, text=f"{kpis['promociones_activas']}", font=("Segoe UI", 18, "bold")).pack()
        # Notebook dentro del área de contenido
        self.notebook = tb.Notebook(self.content)
        self.notebook.pack(fill="both", expand=True)

        # --- Pestañas según rol ---
        if self.user["rol"] == "admin":
            # Productos
            productos_controller = ProductosController(
                conn_factory=self.controller.conn_factory,
                on_info=self.controller.on_info,
                on_error=self.controller.on_error
            )
            with SafeConnection(lambda: self.controller.conn_factory()) as conn:
                proveedores = [(p["id_proveedor"], p["nombre"]) for p in proveedores_repo.list_proveedores(conn)]
            self.productos_view = ProductosView(self.notebook, productos_controller, proveedores)
            self.notebook.add(self.productos_view, text="Productos")

            # Proveedores
            proveedores_controller = ProveedoresController(
                conn_factory=self.controller.conn_factory,
                on_info=self.controller.on_info,
                on_error=self.controller.on_error
            )
            self.notebook.add(ProveedoresView(self.notebook, proveedores_controller), text="Proveedores")

            # Entradas
            entradas_controller = EntradasController(
                conn_factory=self.controller.conn_factory,
                on_info=self.controller.on_info,
                on_error=self.controller.on_error,
                on_productos_updated=self.refrescar_productos
            )
            with self.controller.conn_factory() as conn:
                proveedores = proveedores_repo.get_all(conn)
                productos = productos_repo.get_all(conn)
            entradas_view = EntradasView(
                self.notebook,
                entradas_controller,
                proveedores,
                productos,
                self.user
            )
            self.notebook.add(entradas_view, text="Entradas")

            # Usuarios
            usuarios_controller = UsuariosController(
                conn_factory=self.controller.conn_factory,
                on_info=self.controller.on_info,
                on_error=self.controller.on_error
            )
            usuarios_view = UsuariosView(self.notebook, usuarios_controller, self.user)
            self.notebook.add(usuarios_view, text="Usuarios")

        # Ventas (visible para todos)
        ventas_controller = VentasController(
            conn_factory=self.controller.conn_factory,
            on_info=self.controller.on_info,
            on_error=self.controller.on_error,
            on_productos_updated=self.refrescar_productos
        )
        self.notebook.add(VentasView(self.notebook, ventas_controller, self.user), text="Ventas")

        # Devoluciones (visible para todos)
        devoluciones_controller = DevolucionesController(
            conn_factory=self.controller.conn_factory,
            on_info=self.controller.on_info,
            on_error=self.controller.on_error
        )
        with self.controller.conn_factory() as conn:
            productos = productos_repo.get_all(conn)
        devoluciones_view = DevolucionesView(
            self.notebook,
            devoluciones_controller,
            productos,
            self.user
        )
        self.notebook.add(devoluciones_view, text="Devoluciones")

    def _select_tab(self, tab_name):
        """Selecciona la pestaña del Notebook según el nombre"""
        for idx in range(len(self.notebook.tabs())):
            if self.notebook.tab(idx, "text") == tab_name:
                self.notebook.select(idx)
                break

    def refrescar_productos(self):
        with SafeConnection(lambda: self.controller.conn_factory()) as conn:
            productos = productos_repo.list_productos(conn)
        self.productos_view.actualizar_productos(productos)

    def _logout(self):
        self.destroy()
        self.on_logout()

    def _crear_backup(self):
        try:
            path = backup.create_backup()
            self.controller.on_info(f"Backup creado en {path}")
        except Exception as e:
            self.controller.on_error(f"Error al crear backup: {e}")

    def _restaurar_backup(self):
        try:
            import glob
            from tkinter import filedialog
            from config.settings import BACKUP_DIR
            from utils import backup

            files = sorted(glob.glob(str(BACKUP_DIR / "inventario_*.db")))
            if not files:
                self.controller.on_error("No hay backups disponibles")
                return

            backup_file = filedialog.askopenfilename(
                title="Seleccionar backup para restaurar",
                initialdir=BACKUP_DIR,
                filetypes=[("Archivos de base de datos", "inventario_*.db")]
            )

            if not backup_file:
                self.controller.on_info("Restauración cancelada por el usuario")
                return

            backup.restore_backup(backup_file)
            self.controller.on_info(f"Backup restaurado correctamente desde {backup_file}")

        except Exception as e:
            self.controller.on_error(f"Error al restaurar backup: {e}")