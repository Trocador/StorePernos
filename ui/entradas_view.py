# ui/entradas_view.py
import tkinter as tk
from tkinter import ttk
from ui import alerts

class EntradasView(tk.Frame):
    def __init__(self, master, controller, proveedores, productos, user):
        super().__init__(master)
        self.controller = controller
        self.proveedores = proveedores   # [(id, nombre), ...]
        self.productos = productos       # [(id, nombre), ...] o [(id, "tipo medida largo"), ...]
        self.user = user
        self._build()

    def _build(self):
        # --- Formulario de registro ---
        # Producto
        tk.Label(self, text="Producto").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.producto_combo = ttk.Combobox(
            self,
            values=[f"{pid} - {nombre}" for pid, nombre in self.productos],
            state="readonly", width=50
        )
        self.producto_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        # permitir expansión
        self.grid_columnconfigure(1, weight=1)

        # Cantidad
        tk.Label(self, text="Cantidad").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.cantidad_var = tk.DoubleVar(value=1)
        tk.Spinbox(self, from_=1, to=1000, textvariable=self.cantidad_var).grid(row=1, column=1)

        # Proveedor
        tk.Label(self, text="Proveedor").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.proveedor_combo = ttk.Combobox(
            self,
            values=[f"{pid} - {nombre}" for pid, nombre in self.proveedores],
            state="readonly"
        )
        self.proveedor_combo.grid(row=2, column=1)

        # Botón registrar
        tk.Button(self, text="Registrar entrada", command=self._registrar).grid(row=3, column=0, columnspan=2, pady=10)

        # --- Listado de entradas ---
        self.tree = ttk.Treeview(
            self,
            columns=("id", "producto", "cantidad", "proveedor", "fecha"),
            show="headings"
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("producto", text="Producto")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("proveedor", text="Proveedor")
        self.tree.heading("fecha", text="Fecha")

        self.tree.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=4, column=2, sticky="ns")

        # Ajustar expansión
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Cargar entradas iniciales
        self._cargar_entradas()

    def _registrar(self):
        producto_texto = self.producto_combo.get()
        proveedor_texto = self.proveedor_combo.get()
        if not producto_texto or not proveedor_texto:
            alerts.error("Debe seleccionar producto y proveedor")
            return

        id_producto = int(producto_texto.split(" - ")[0])
        id_proveedor = int(proveedor_texto.split(" - ")[0])

        ok = self.controller.registrar(
            id_producto,
            self.cantidad_var.get(),
            id_proveedor,
            self.user["id_usuario"]
        )
        if ok:
            alerts.info("Entrada registrada correctamente")
            self._cargar_entradas()
        else:
            alerts.error("Error al registrar entrada")

    def _cargar_entradas(self):
        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        entradas = self.controller.listar()
        for e in entradas:
            self.tree.insert("", "end", values=(
                e["id_entrada"],
                e["producto"],   # nombre del producto desde JOIN
                e["cantidad"],
                e["proveedor"],  # nombre del proveedor desde JOIN
                e["fecha"]
            ))