# ui/productos_view.py
import tkinter as tk
from tkinter import ttk
from ui import alerts

class ProductosView(tk.Frame):
    def __init__(self, master, controller, proveedores):
        super().__init__(master)
        self.controller = controller
        self.proveedores = proveedores
        self._build()

    def _build(self):
        # --- Formulario de creación ---
        tk.Label(self, text="Tipo de producto").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tipos = ["tuerca", "perno", "tornillo", "varilla", "remache", "arandela"]
        self.tipo_var = tk.StringVar(value=tipos[0])
        ttk.Combobox(self, textvariable=self.tipo_var, values=tipos, state="readonly").grid(row=0, column=1)

        tk.Label(self, text="Abreviatura").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.medida_var = tk.StringVar(value="M8")
        tk.Entry(self, textvariable=self.medida_var).grid(row=1, column=1)

        tk.Label(self, text="Cabeza y métrica").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.largo_var = tk.StringVar(value="30mm")
        tk.Entry(self, textvariable=self.largo_var).grid(row=2, column=1)

        tk.Label(self, text="Material").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.material_var = tk.StringVar(value="acero")
        tk.Entry(self, textvariable=self.material_var).grid(row=3, column=1)

        tk.Label(self, text="Precio unidad").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.precio_unidad_var = tk.DoubleVar(value=0.0)
        tk.Entry(self, textvariable=self.precio_unidad_var).grid(row=4, column=1)

        tk.Label(self, text="Precio kilo").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.precio_kilo_var = tk.DoubleVar(value=0.0)
        tk.Entry(self, textvariable=self.precio_kilo_var).grid(row=5, column=1)

        tk.Label(self, text="Stock inicial").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.stock_var = tk.IntVar(value=1)
        tk.Spinbox(self, from_=0, to=1000, textvariable=self.stock_var).grid(row=6, column=1)

        tk.Label(self, text="Stock mínimo").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.stock_minimo_var = tk.IntVar(value=0)
        tk.Spinbox(self, from_=0, to=1000, textvariable=self.stock_minimo_var).grid(row=7, column=1)

        tk.Label(self, text="Proveedor").grid(row=8, column=0, sticky="e", padx=5, pady=5)
        proveedores_nombres = [f"{pid} - {nombre}" for pid, nombre in self.proveedores]
        self.proveedor_combo = ttk.Combobox(self, values=proveedores_nombres, state="readonly")
        self.proveedor_combo.grid(row=8, column=1)

        tk.Button(self, text="Crear producto", command=self._crear).grid(row=9, column=0, columnspan=2, pady=10)

        # --- Listado de productos ---
        self.tree = ttk.Treeview(self, columns=(
            "tipo", "medida", "largo", "material",
            "precio_unidad", "precio_kilo",
            "stock", "stock_minimo", "proveedor"
        ), show="headings")

        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("medida", text="Abreviatura")
        self.tree.heading("largo", text="Cabeza y metrica")
        self.tree.heading("material", text="Material")
        self.tree.heading("precio_unidad", text="Precio Unidad")
        self.tree.heading("precio_kilo", text="Precio Kilo")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("stock_minimo", text="Stock Mínimo")
        self.tree.heading("proveedor", text="Proveedor")


        self.tree.grid(row=10, column=0, columnspan=2, sticky="nsew", pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=10, column=2, sticky="ns")

        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._cargar_productos()

    def _crear(self):
        tipo = self.tipo_var.get().lower()
        medida = self.medida_var.get()
        largo = self.largo_var.get()
        material = self.material_var.get()
        precio_unidad = self.precio_unidad_var.get()
        precio_kilo = self.precio_kilo_var.get()
        stock = self.stock_var.get()
        stock_minimo = self.stock_minimo_var.get()

        proveedor_texto = self.proveedor_combo.get()
        if not proveedor_texto:
            alerts.error("Debe seleccionar un proveedor")
            return
        id_proveedor = int(proveedor_texto.split(" - ")[0])

        ok = self.controller.crear(tipo, medida, largo, material, precio_unidad, precio_kilo, stock, stock_minimo, id_proveedor)
        if ok:
            alerts.info("Producto creado correctamente")
            self._cargar_productos()
        else:
            alerts.error("Error al crear producto")

    def _cargar_productos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        productos = self.controller.listar()
        for row in productos:
            self.tree.insert("", "end", values=(
            row["tipo"], row["medida"], row["largo"], row["material"],
            row["precio_unidad"], row["precio_kilo"],
            row["stock"], row["stock_minimo"], row["proveedor"]  # ✅ nombre
        ))

    def actualizar_productos(self, productos):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in productos:
            self.tree.insert("", "end", values=(
                p["tipo"], p["medida"], p["largo"], p["material"],
                p["precio_unidad"], p["precio_kilo"],
                p["stock"], p["stock_minimo"], p["proveedor"]
            ))
