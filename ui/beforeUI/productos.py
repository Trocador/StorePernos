# ui/productos.py
import tkinter as tk
from tkinter import messagebox
from database.connection import get_connection
from database.repositories import productos_repo

def productos_ui(user_data):
    ventana = tk.Toplevel()
    ventana.title("Gestión de Productos")

    tk.Label(ventana, text="ID Producto").grid(row=0, column=0)
    id_entry = tk.Entry(ventana)
    id_entry.grid(row=0, column=1)

    tk.Label(ventana, text="Tipo").grid(row=1, column=0)
    tipo_entry = tk.Entry(ventana)
    tipo_entry.grid(row=1, column=1)

    tk.Label(ventana, text="Medida").grid(row=2, column=0)
    medida_entry = tk.Entry(ventana)
    medida_entry.grid(row=2, column=1)

    tk.Label(ventana, text="Precio").grid(row=3, column=0)
    precio_entry = tk.Entry(ventana)
    precio_entry.grid(row=3, column=1)

    def crear_producto():
        with get_connection() as conn:
            productos_repo.create_producto(conn, (
                tipo_entry.get(), medida_entry.get(), None, None,
                float(precio_entry.get()), 0, 0
            ))
        messagebox.showinfo("Éxito", "Producto creado")

    tk.Button(ventana, text="Crear", command=crear_producto).grid(row=4, column=0, columnspan=2, pady=10)