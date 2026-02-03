# ui/devoluciones_view.py
import tkinter as tk
from tkinter import ttk
import tkcalendar
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
        # --- Selección de fecha ---
        tk.Label(self, text="Fecha de venta").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.fecha_var = tk.StringVar()
        self.fecha_entry = tkcalendar.DateEntry(self, textvariable=self.fecha_var, date_pattern="yyyy-mm-dd")
        self.fecha_entry.grid(row=0, column=1)

        tk.Button(self, text="Buscar ventas", command=self._buscar_ventas).grid(row=0, column=2, padx=5)

        # --- Tabla de ventas del día ---
        self.tree_ventas = ttk.Treeview(
            self,
            columns=("idVenta", "fecha", "total"),
            show="headings"
        )
        for col in ("idVenta", "fecha", "total"):
            self.tree_ventas.heading(col, text=col.capitalize())
        self.tree_ventas.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)
        # Boton buscar producto
        tk.Button(self, text="Buscar producto", command=self._abrir_buscador).grid(row=2, column=2, padx=5)
        self.producto_var = tk.StringVar(value="(ningún producto seleccionado)")
        tk.Label(self, text="Producto seleccionado:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.producto_label = tk.Label(self, textvariable=self.producto_var, anchor="w", width=50, relief="sunken")
        self.producto_label.grid(row=2, column=1, sticky="ew", padx=5, pady=5)


        tk.Label(self, text="Cantidad").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.cantidad_var = tk.DoubleVar(value=1)
        tk.Spinbox(self, from_=1, to=1000, textvariable=self.cantidad_var).grid(row=3, column=1)
        tk.Label(self, text="Observación").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.obs_var = tk.StringVar()
        tk.Entry(self, textvariable=self.obs_var).grid(row=4, column=1)
        #check
        self.confusion_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Confusión sin daño (reinsertar stock)", variable=self.confusion_var).grid(row=5, column=1, sticky="w", pady=5)
        tk.Button(self, text="Registrar devolución", command=self._registrar).grid(row=5, column=1, columnspan=2, pady=10)
        # --- Listado de devoluciones ---
        self.tree_devoluciones = ttk.Treeview(
            self,
            columns=("idDevolucion", "venta", "fecha", "usuario", "obs"),
            show="headings"
        )
        for col in ("idDevolucion", "venta", "fecha", "usuario", "obs"):
            self.tree_devoluciones.heading(col, text=col.capitalize())
        self.tree_devoluciones.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

        # --- Listado de detalle ---
        self.tree_detalle = ttk.Treeview(
            self,
            columns=("idProducto","producto","cantidad"),
            show="headings"
        )
        self.tree_detalle.heading("idProducto", text="ID Producto")
        self.tree_detalle.heading("producto", text="Producto")
        self.tree_detalle.heading("cantidad", text="Cantidad")
        self.tree_detalle.grid(row=7, column=0, columnspan=2, sticky="nsew", pady=10)

        self.tree_devoluciones.bind("<<TreeviewSelect>>", self._mostrar_detalle)

        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._cargar_devoluciones()

    def _registrar(self):
        producto_texto = self.producto_var.get()
        if not producto_texto:
            alerts.error("Seleccione producto")
            return
        id_producto = int(producto_texto.split(" - ")[0])

        # 🔥 Obtener id_venta desde la tabla de ventas seleccionada
        selected = self.tree_ventas.selection()
        if not selected:
            alerts.error("Debe seleccionar una venta de la tabla")
            return
        id_venta = self.tree_ventas.item(selected[0])["values"][0]

        ok = self.controller.registrar(
            id_venta,
            id_producto,
            self.cantidad_var.get(),
            self.user["id_usuario"],
            self.obs_var.get(),
            reinserta_stock=self.confusion_var.get()
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
            # 🔥 Ahora insertamos también el id_producto
            self.tree_detalle.insert("", "end", values=(det["id_producto"], det["producto"], det["cantidad"]))
    
    def _buscar_ventas(self):
        fecha = self.fecha_var.get()
        ventas = self.controller.ventas_por_fecha(fecha)

        for row in self.tree_ventas.get_children():
            self.tree_ventas.delete(row)

        for v in ventas:
            self.tree_ventas.insert("", "end", values=(v["id_venta"], v["fecha"], v["total"]))

    def _abrir_buscador(self):
        popup = tk.Toplevel(self)
        popup.title("Buscar producto")
        popup.geometry("700x400")

        tk.Label(popup, text="Filtrar:").pack(pady=5)
        filtro_var = tk.StringVar()
        filtro_entry = tk.Entry(popup, textvariable=filtro_var)
        filtro_entry.pack(fill="x", padx=10)

        tree = ttk.Treeview(popup, columns=("id", "nombre", "stock"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("nombre", text="Producto")
        tree.heading("stock", text="Stock")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        productos = self.controller.listar_productos()

        def cargar_productos(filtro=""):
            for row in tree.get_children():
                tree.delete(row)
            for p in productos:
                nombre = f"{p['tipo']} {p['medida']} {p['largo'] or ''}"
                if filtro.lower() in nombre.lower():
                    tree.insert("", "end", values=(p["id_producto"], nombre, p["stock"]))

        cargar_productos()

        # Filtrado automático al escribir
        filtro_var.trace_add("write", lambda *args: cargar_productos(filtro_var.get()))

        # Botón opcional para filtrar manualmente
        def aplicar_filtro():
            cargar_productos(filtro_var.get())
        tk.Button(popup, text="Filtrar", command=aplicar_filtro).pack(pady=5)

        def seleccionar():
            sel = tree.selection()
            if sel:
                values = tree.item(sel[0])["values"]
                self.producto_var.set(f"{values[0]} - {values[1]}")
                popup.destroy()

        tk.Button(popup, text="Seleccionar", command=seleccionar).pack(pady=5)