# ui/dashboard_view.py
import tkinter as tk
from tkinter import ttk
from ui.productos_view import ProductosView
from ui.ventas_view import VentasView
from ui.entradas_view import EntradasView
from ui.devoluciones_view import DevolucionesView
from ui.usuarios_view import UsuariosView
from ui.usuarios_controller import UsuariosController
from ui.entradas_controller import EntradasController
from ui.entradas_view import EntradasView
from ui.devoluciones_controller import DevolucionesController
from ui.login_view import LoginView
from ui.productos_controller import ProductosController
from ui.ventas_controller import VentasController
from ui.proveedores_controller import ProveedoresController
from ui.proveedores_view import ProveedoresView
from utils import backup
from utils.db import SafeConnection
from utils.backup import create_backup, restore_backup
from database.repositories import proveedores_repo, productos_repo

class DashboardView(tk.Frame):
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

        # --- Notebook con pestañas ---
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

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
            self.productos_view = ProductosView(notebook, productos_controller, proveedores)
            notebook.add(self.productos_view, text="Productos")

            # Proveedores
            proveedores_controller = ProveedoresController(
                conn_factory=self.controller.conn_factory,
                on_info=self.controller.on_info,
                on_error=self.controller.on_error
            )
            notebook.add(ProveedoresView(notebook, proveedores_controller), text="Proveedores")

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
                notebook,
                entradas_controller,
                proveedores,
                productos,
                self.user
            )
            notebook.add(entradas_view, text="Entradas")

            # Usuarios
            usuarios_controller = UsuariosController(
                conn_factory=self.controller.conn_factory,
                on_info=self.controller.on_info,
                on_error=self.controller.on_error
            )
            usuarios_view = UsuariosView(notebook, usuarios_controller, self.user)
            notebook.add(usuarios_view, text="Usuarios")

        # Ventas (visible para todos)
        ventas_controller = VentasController(
            conn_factory=self.controller.conn_factory,
            on_info=self.controller.on_info,
            on_error=self.controller.on_error,
            on_productos_updated=self.refrescar_productos
        )
        notebook.add(VentasView(notebook, ventas_controller, self.user), text="Ventas")

        # Devoluciones (visible para todos)
        devoluciones_controller = DevolucionesController(
            conn_factory=self.controller.conn_factory,
            on_info=self.controller.on_info,
            on_error=self.controller.on_error
        )
        with self.controller.conn_factory() as conn:
            productos = productos_repo.get_all(conn)
        devoluciones_view = DevolucionesView(
            notebook,
            devoluciones_controller,
            productos,
            self.user
        )
        notebook.add(devoluciones_view, text="Devoluciones")

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

            #  Buscar todos los backups disponibles
            files = sorted(glob.glob(str(BACKUP_DIR / "inventario_*.db")))
            if not files:
                self.controller.on_error("No hay backups disponibles")
                return

            #  Abrir diálogo para que el usuario elija el backup
            backup_file = filedialog.askopenfilename(
                title="Seleccionar backup para restaurar",
                initialdir=BACKUP_DIR,
                filetypes=[("Archivos de base de datos", "inventario_*.db")]
            )

            if not backup_file:
                self.controller.on_info("Restauración cancelada por el usuario")
                return

            #  Restaurar el backup seleccionado
            backup.restore_backup(backup_file)
            self.controller.on_info(f"Backup restaurado correctamente desde {backup_file}")

        except Exception as e:
            self.controller.on_error(f"Error al restaurar backup: {e}")