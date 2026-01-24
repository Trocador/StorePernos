# ui/devoluciones_view.py
import tkinter as tk
from tkinter import ttk
from ui import alerts

class DevolucionesView(tk.Frame):
    def __init__(self, master, controller, productos, user):
        super().__init__(master)
        self.controller = controller
        self.productos = productos   # [(id, nombre), ...]
        self.user = user
        self.detalle_actual = []
        self._build()

    def _build(self):
        # --- Formulario de registro ---
        tk.Label(self, text="ID Venta").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.id_venta_var = tk.IntVar(value=1)
        tk.Spinbox(self, from_=1, to=9999, textvariable=self.id_venta_var).grid(row=0, column=1)

        tk.Label(self, text="Producto").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.producto_combo = ttk.Combobox(
            self,
            values=[f"{pid} - {nombre}" for pid, nombre in self.productos],
            state="readonly"
        )
        self.producto_combo.grid(row=1, column=1)

        tk.Label(self, text="Cantidad").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.cantidad_var = tk.DoubleVar(value=1)
        tk.Spinbox(self, from_=1, to=1000, textvariable=self.cantidad_var).grid(row=2, column=1)

        tk.Label(self, text="Observación").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.obs_var = tk.StringVar()
        tk.Entry(self, textvariable=self.obs_var).grid(row=3, column=1)

        tk.Button(self, text="Registrar devolución", command=self._registrar).grid(row=4, column=0, columnspan=2, pady=10)

        # --- Listado de devoluciones ---
        self.tree_devoluciones = ttk.Treeview(
            self,
            columns=("idDevolucion", "venta", "fecha", "usuario", "obs"),
            show="headings"
        )
        for col in ("idDevolucion", "venta", "fecha", "usuario", "obs"):
            self.tree_devoluciones.heading(col, text=col.capitalize())
        self.tree_devoluciones.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=10)

        # --- Listado de detalle ---
        self.tree_detalle = ttk.Treeview(
            self,
            columns=("producto","cantidad"),
            show="headings"
        )
        self.tree_detalle.heading("producto", text="Producto")
        self.tree_detalle.heading("cantidad", text="Cantidad")
        self.tree_detalle.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

        self.tree_devoluciones.bind("<<TreeviewSelect>>", self._mostrar_detalle)

        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._cargar_devoluciones()

    def _registrar(self):
        producto_texto = self.producto_combo.get()
        if not producto_texto:
            alerts.error("Seleccione producto")
            return
        id_producto = int(producto_texto.split(" - ")[0])

        ok = self.controller.registrar(
            self.id_venta_var.get(),
            id_producto,
            self.cantidad_var.get(),
            self.user["id_usuario"],
            self.obs_var.get()
        )
        if ok:
            alerts.info("Devolución registrada correctamente")
            self._cargar_devoluciones()
        else:
            alerts.error("Error al registrar devolución")

    def _cargar_devoluciones(self):
        for row in self.tree_devoluciones.get_children():
            self.tree_devoluciones.delete(row)

        devoluciones = self.controller.listar()
        for d in devoluciones:
            self.tree_devoluciones.insert("", "end", values=(
                d["id_devolucion"],
                d["id_venta"],
                d["fecha"],
                d["id_usuario"],
                d["observacion"]
            ))

    def _mostrar_detalle(self, event):
        for row in self.tree_detalle.get_children():
            self.tree_detalle.delete(row)

        selected = self.tree_devoluciones.selection()
        if not selected:
            return
        id_devolucion = self.tree_devoluciones.item(selected[0])["values"][0]

        detalles = self.controller.detalle(id_devolucion)
        for det in detalles:
            self.tree_detalle.insert("", "end", values=(det["producto"], det["cantidad"]))