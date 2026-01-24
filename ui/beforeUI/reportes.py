# ui/reportes.py
import tkinter as tk
from database.connection import get_connection
from database.repositories import ventas_repo, movimientos_repo

def reportes_ui(user_data):
    ventana = tk.Toplevel()
    ventana.title("Reportes")

    tk.Label(ventana, text="Fecha inicio (YYYY-MM-DD)").grid(row=0, column=0)
    inicio_entry = tk.Entry(ventana)
    inicio_entry.grid(row=0, column=1)

    tk.Label(ventana, text="Fecha fin (YYYY-MM-DD)").grid(row=1, column=0)
    fin_entry = tk.Entry(ventana)
    fin_entry