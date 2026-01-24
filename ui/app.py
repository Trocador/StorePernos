# ui/app.py
import tkinter as tk
from utils.db import SafeConnection, create_connection
from ui.login_view import LoginView
from ui.login_controller import LoginController
from ui.dashboard_view import DashboardView
from ui.dashboard_controller import DashboardController
from tkinter import messagebox

conn_factory = create_connection

class App(tk.Tk):
    def __init__(self, conn_factory):
        super().__init__()
        self.title("Tienda Pernos")
        self.geometry("1800x700")

        # ✅ guardar la fábrica de conexiones
        self.conn_factory = conn_factory

        # siempre inicia con login
        self._show_login()

    def _show_login(self):
        # limpiar cualquier frame previo
        for widget in self.winfo_children():
            widget.destroy()

        login_controller = LoginController(
            conn_factory=self.conn_factory,
            on_success=self._show_dashboard,
        )
        login_view = LoginView(self, login_controller)
        login_view.pack(fill="both", expand=True)

    def _show_dashboard(self, user):
        # limpiar cualquier frame previo
        for widget in self.winfo_children():
            widget.destroy()

        dashboard_controller = DashboardController(
            conn_factory=self.conn_factory,
            on_info=self._show_info,
            on_error=self._show_error
        )
        dash_view = DashboardView(self, dashboard_controller, user, on_logout=self._show_login)
        dash_view.pack(fill="both", expand=True)

    # Métodos auxiliares para mensajes
    def _show_info(self, msg):
        print("INFO:", msg)

    def _show_error(self, msg):
        print("ERROR:", msg)

if __name__ == "__main__":
    App(conn_factory).mainloop()