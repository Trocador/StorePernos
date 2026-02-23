# ui/login_view.py
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
class LoginView(tb.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self._build()

    def _build(self):
        # Contenedor principal
        self.main = tb.Frame(self, padding=40)
        self.main.pack(expand=True)

        # Tarjeta estilo moderno
        card = tb.Frame(self.main, bootstyle="light", padding=30)
        card.pack()

        # Usuario
        tb.Label(card, text="Usuario").pack(fill="x", pady=5)
        self.entry_usuario = tb.Entry(card)
        self.entry_usuario.pack(fill="x", pady=5)

        # Contraseña
        tb.Label(card, text="Contraseña").pack(fill="x", pady=5)
        self.entry_password = tb.Entry(card, show="*")
        self.entry_password.pack(fill="x", pady=5)

        # Botón ingresar
        tb.Button(card, text="Ingresar", bootstyle="success-outline", command=self._intentar_login).pack(fill="x", pady=10)

    def _intentar_login(self):
        ok = self.controller.login(
            self.entry_usuario.get(),
            self.entry_password.get()
        )
        if ok:
            Messagebox.show_info(message="Login correcto", title="OK")
        else:
            Messagebox.show_error(message="Credenciales inválidas", title="Error")