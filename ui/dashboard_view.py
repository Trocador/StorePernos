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
from utils.db import SafeConnection
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

        tk.Label(top_bar, text=f"Usuario: {self.user['id_usuario']} ({self.user['rol']})").pack(side="left", padx=10)
        tk.Button(top_bar, text="Cerrar sesión", command=self._logout).pack(side="right", padx=10)

        # --- Notebook con pestañas ---
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # aquí añades tus pestañas (Entradas, Devoluciones, Usuarios, etc.)
        # notebook.add(...)

        # Productos
        productos_controller = ProductosController(
            conn_factory=self.controller.conn_factory,
            on_info=self.controller.on_info,
            on_error=self.controller.on_error
        )
        with SafeConnection(lambda: self.controller.conn_factory()) as conn:
            proveedores = [(p["id_proveedor"], p["nombre"]) for p in proveedores_repo.list_proveedores(conn)]
        notebook.add(ProductosView(notebook, productos_controller, proveedores), text="Productos")
        
        
        # Proveedores
        proveedores_controller = ProveedoresController(
        conn_factory=self.controller.conn_factory,
        on_info=self.controller.on_info,
        on_error=self.controller.on_error
        )
        notebook.add(ProveedoresView(notebook, proveedores_controller), text="Proveedores")

        # Ventas
        ventas_controller = VentasController(
            conn_factory=self.controller.conn_factory,
            on_info=self.controller.on_info,
            on_error=self.controller.on_error
        )
        notebook.add(VentasView(notebook, ventas_controller, self.user), text="Ventas")

        # --- Entradas ---
        entradas_controller = EntradasController(
            conn_factory=self.controller.conn_factory,
            on_info=self.controller.on_info,
            on_error=self.controller.on_error
        )
        # ✅ obtener proveedores y productos
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

        # --- Devoluciones ---
        devoluciones_controller = DevolucionesController(
            conn_factory=self.controller.conn_factory,
            on_info=self.controller.on_info,
            on_error=self.controller.on_error
        )

        # ✅ obtener productos para el combo
        with self.controller.conn_factory() as conn:
            productos = productos_repo.get_all(conn)

        devoluciones_view = DevolucionesView(
            notebook,
            devoluciones_controller,
            productos,
            self.user
        )
        notebook.add(devoluciones_view, text="Devoluciones")

        # --- Usuarios ---
        if self.user["rol"] == "admin":   # ✅ solo admin puede ver esta pestaña
            usuarios_controller = UsuariosController(
                conn_factory=self.controller.conn_factory,
                on_info=self.controller.on_info,
                on_error=self.controller.on_error
            )
            usuarios_view = UsuariosView(notebook, usuarios_controller, self.user)
            notebook.add(usuarios_view, text="Usuarios")
    def _logout(self):
        # Destruir dashboard y volver al login
        self.destroy()
        self.on_logout()
