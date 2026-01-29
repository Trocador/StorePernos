# ui/ventas_view.py
import tkinter as tk
from tkinter import ttk
from ui import alerts

class VentasView(tk.Frame):
    def __init__(self, master, controller, user):
        super().__init__(master)
        self.controller = controller
        self.user = user
        self.detalle_actual = []  # lista temporal de items antes de guardar
        self._build()

    def _build(self):
        # --- Formulario de registro ---
        tk.Label(self, text="Producto").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        productos = self.controller.listar_productos()
        productos_nombres = [f"{p['id_producto']} - {p['tipo']} {p['medida']} {p['largo']}" for p in productos]
        self.producto_combo = ttk.Combobox(self, values=productos_nombres, state="readonly")
        self.producto_combo.grid(row=0, column=1)

        tk.Label(self, text="Cantidad").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.cantidad_var = tk.IntVar(value=1)
        tk.Spinbox(self, from_=1, to=1000, textvariable=self.cantidad_var).grid(row=1, column=1)

        tk.Label(self, text="Total a pagar").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.total_var = tk.DoubleVar(value=0.0)
        tk.Entry(self, textvariable=self.total_var, state="readonly").grid(row=2, column=1)

        tk.Label(self, text="Tipo venta").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.tipo_venta_var = tk.StringVar(value="unidad")
        ttk.Combobox(self, textvariable=self.tipo_venta_var, values=["unidad","kilo"], state="readonly").grid(row=3, column=1)

        tk.Button(self, text="Agregar ítem", command=self._agregar_item).grid(row=4, column=0, pady=10)
        tk.Button(self, text="Resetear ítems", command=self._reset_items).grid(row=4, column=1, pady=10)
        tk.Button(self, text="Finalizar venta", command=self._registrar).grid(row=4, column=2, pady=10)
        # --- Listado de ventas ---
        self.tree_ventas = ttk.Treeview(self, columns=("id", "usuario", "fecha", "total"), show="headings")
        self.tree_ventas.heading("id", text="ID Venta")
        self.tree_ventas.heading("usuario", text="Usuario")
        self.tree_ventas.heading("fecha", text="Fecha")
        self.tree_ventas.heading("total", text="Total")
        self.tree_ventas.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=10)

        scrollbar1 = ttk.Scrollbar(self, orient="vertical", command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscroll=scrollbar1.set)
        scrollbar1.grid(row=5, column=2, sticky="ns")

        # --- Listado de detalle ---
        self.tree_detalle = ttk.Treeview(
            self,
            columns=("id_detalle", "id_producto", "producto", "cantidad", "tipo_venta", "precio_unitario", "subtotal"),
            show="headings"
        )
        self.tree_detalle.heading("id_detalle", text="ID Detalle")
        self.tree_detalle.heading("id_producto", text="ID Producto")
        self.tree_detalle.heading("producto", text="Producto")
        self.tree_detalle.heading("cantidad", text="Cantidad")
        self.tree_detalle.heading("tipo_venta", text="Tipo Venta")
        self.tree_detalle.heading("precio_unitario", text="Precio Unitario")
        self.tree_detalle.heading("subtotal", text="Subtotal")
        self.tree_detalle.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

        scrollbar2 = ttk.Scrollbar(self, orient="vertical", command=self.tree_detalle.yview)
        self.tree_detalle.configure(yscroll=scrollbar2.set)
        scrollbar2.grid(row=6, column=2, sticky="ns")

        # Configuración de expansión
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Evento de selección
        self.tree_ventas.bind("<<TreeviewSelect>>", self._mostrar_detalle)

        # Cargar ventas iniciales
        self._cargar_ventas()

    def _agregar_item(self):
        seleccionado = self.producto_combo.get()
        if not seleccionado:
            alerts.error("Debe seleccionar un producto")
            return
        id_producto = int(seleccionado.split(" - ")[0])
        producto = self.controller.get_producto(id_producto)
        if self.tipo_venta_var.get() == "unidad":
            precio = producto["precio_unidad"]
        else:
            precio = producto["precio_kilo"]
        item = {
            "id_producto": id_producto,
            "cantidad": self.cantidad_var.get(),
            "tipo_venta": self.tipo_venta_var.get(),
            "precio_unitario": precio,
            "subtotal": self.cantidad_var.get() * precio
        }
        
        # 🔥 Agregar ítem a la lista
        self.detalle_actual.append(item)
        # 🔥 Actualizar el total acumulado en el campo "Total a pagar"
        self.total_var.set(sum(i["subtotal"] for i in self.detalle_actual))
        # Mostrar aviso
        alerts.info(f"Item agregado: {item}")

    def _registrar(self):
        if not self.detalle_actual:
            alerts.error("Debe agregar al menos un ítem")
            return

        ok = self.controller.registrar(self.user["id_usuario"], self.detalle_actual)
        if ok:
            alerts.info("Venta registrada correctamente")
            self.detalle_actual.clear()
            self.total_var.set(0.0)
            self._cargar_ventas()
        else:
            alerts.error("Error al registrar venta")

    def _cargar_ventas(self):
        for row in self.tree_ventas.get_children():
            self.tree_ventas.delete(row)

        ventas = self.controller.listar()
        for v in ventas:
            self.tree_ventas.insert("", "end", values=(v["id_venta"], v["id_usuario"], v["fecha"], v["total"]))

    def _mostrar_detalle(self, event):
        for row in self.tree_detalle.get_children():
            self.tree_detalle.delete(row)

        selected = self.tree_ventas.selection()
        if not selected:
            return
        id_venta = self.tree_ventas.item(selected[0])["values"][0]

        detalles = self.controller.detalle(id_venta)
        for d in detalles:
            self.tree_detalle.insert("", "end", values=(
                d["id_detalle"],
                d["id_producto"],
                d["producto"],   # 🔥 ahora muestra nombre
                d["cantidad"],
                d["tipo_venta"],
                d["precio_unitario"],
                d["subtotal"]
            ))

    def _reset_items(self):
        self.detalle_actual.clear()
        self.total_var.set(0.0)
        alerts.info("Ítems de la venta reseteados")