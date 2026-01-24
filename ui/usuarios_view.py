# ui/usuarios_view.py
import tkinter as tk
from tkinter import ttk
from ui import alerts

class UsuariosView(tk.Frame):
    def __init__(self, master, controller, user):
        super().__init__(master)
        self.controller = controller
        self.user = user
        self._build()

    def _build(self):
        # --- Formulario de creación de usuario ---
        tk.Label(self, text="Usuario").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.username_var = tk.StringVar()
        tk.Entry(self, textvariable=self.username_var).grid(row=0, column=1)

        tk.Label(self, text="Contraseña").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.password_var = tk.StringVar()
        tk.Entry(self, textvariable=self.password_var, show="*").grid(row=1, column=1)

        tk.Label(self, text="Rol").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.rol_combo = ttk.Combobox(
            self,
            values=["admin", "vendedor"],  # ✅ solo dos roles
            state="readonly"
        )
        self.rol_combo.grid(row=2, column=1)

        tk.Button(self, text="Crear usuario", command=self._crear_usuario).grid(row=3, column=0, columnspan=2, pady=10)

        # --- Listado de usuarios ---
        self.tree = ttk.Treeview(
            self,
            columns=("id_usuario", "usuario", "rol"),
            show="headings"
        )
        self.tree.heading("id_usuario", text="ID Usuario")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("rol", text="Rol")
        self.tree.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=4, column=2, sticky="ns")

        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._cargar_usuarios()

    def _crear_usuario(self):
        username = self.username_var.get()
        password = self.password_var.get()
        rol = self.rol_combo.get()

        if not username or not password or not rol:
            alerts.error("Debe completar todos los campos")
            return

        ok = self.controller.crear_usuario(username, password, rol)
        if ok:
            alerts.info("Usuario creado correctamente")
            self._cargar_usuarios()
        else:
            alerts.error("Error al crear usuario")

    def _cargar_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        usuarios = self.controller.listar()
        for u in usuarios:
            self.tree.insert("", "end", values=(u["id_usuario"], u["usuario"], u["rol"]))