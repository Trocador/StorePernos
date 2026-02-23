# ui/proveedores_view.py
import tkinter as tk
import ttkbootstrap as tb
from ui import alerts

class ProveedoresView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self._build()

    def _build(self):
        # --- Formulario ---
        tk.Label(self, text="Nombre").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.nombre_var = tk.StringVar()
        tk.Entry(self, textvariable=self.nombre_var).grid(row=0, column=1)

        tk.Label(self, text="Contacto").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.contacto_var = tk.StringVar()
        tk.Entry(self, textvariable=self.contacto_var).grid(row=1, column=1)

        tb.Button(self, text="Agregar proveedor", bootstyle="success", command=self._crear).grid(row=2, column=0, columnspan=2, pady=10)

        # --- Listado ---
        self.tree = tb.Treeview(self, columns=("id", "nombre", "contacto", "activo"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("contacto", text="Contacto")
        self.tree.heading("activo", text="Activo")
        self.tree.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.tree.tag_configure("oddrow", background="#f8f9fa")
        self.tree.tag_configure("evenrow", background="#ffffff")

        scrollbar = tb.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=3, column=2, sticky="ns")

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._cargar()

    def _crear(self):
        ok = self.controller.crear(self.nombre_var.get(), self.contacto_var.get())
        if ok:
            alerts.info("Proveedor agregado")
            self._cargar()
        else:
            alerts.error("Error al agregar proveedor")

    def _cargar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        proveedores = self.controller.listar()
        for index, p in enumerate(proveedores):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(p["id_proveedor"], p["nombre"], p["contacto"], p["activo"]), tags=(tag,))