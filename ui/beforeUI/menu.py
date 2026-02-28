# ui/menu.py
import tkinter as tk
from ui.ventas_view import ventas_ui
from ui.productos_view import productos_ui
from ui.entradas_view import entradas_ui

def menu_ui(user_data):
    root = tk.Tk()
    root.title("Inventario Pernos - Menú Principal")

    tk.Label(root, text=f"Usuario: {user_data['id_usuario']} | Rol: {user_data['rol']}").pack(pady=10)

    tk.Button(root, text="Ventas", width=20, command=lambda: ventas_ui(user_data)).pack(pady=5)
    tk.Button(root, text="Productos", width=20, command=lambda: productos_ui(user_data)).pack(pady=5)
    tk.Button(root, text="Entradas", width=20, command=lambda: entradas_ui(user_data)).pack(pady=5)
    tk.Button(root, text="Salir", width=20, command=root.destroy).pack(pady=5)

    root.mainloop()