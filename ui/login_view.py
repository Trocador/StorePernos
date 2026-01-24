# ui/login_view.py
import tkinter as tk
from tkinter import messagebox

class LoginView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self._build()

    def _build(self):
        # centrar los widgets dentro
        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="Usuario").grid(row=0, column=0, padx=5, pady=5)
        self.entry_usuario = tk.Entry(container)
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(container, text="Contraseña").grid(row=1, column=0, padx=5, pady=5)
        self.entry_password = tk.Entry(container, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(container, text="Ingresar", command=self._intentar_login).grid(row=2, column=0, columnspan=2, pady=10)

    def _intentar_login(self):
        ok = self.controller.login(
            self.entry_usuario.get(),
            self.entry_password.get()
        )
        if ok:
            messagebox.showinfo("OK", "Login correcto")
        else:
            messagebox.showerror("Error", "Credenciales inválidas")