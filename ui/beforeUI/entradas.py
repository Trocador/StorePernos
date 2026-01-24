# ui/entradas.py
import tkinter as tk
from tkinter import messagebox
from services.entradas_service import registrar_entrada

def entradas_ui(user_data):
    ventana = tk.Toplevel()
    ventana.title("Registrar Entrada")

    detalles = []

    tk.Label(ventana, text="ID Proveedor").grid(row=0, column=0)
    proveedor_entry = tk.Entry(ventana)
    proveedor_entry.grid(row=0, column=1)

    tk.Label(ventana, text="Observación").grid(row=1, column=0)
    obs_entry = tk.Entry(ventana)
    obs_entry.grid(row=1, column=1)

    tk.Label(ventana, text="ID Producto").grid(row=2, column=0)
    producto_entry = tk.Entry(ventana)
    producto_entry.grid(row=2, column=1)

    tk.Label(ventana, text="Cantidad").grid(row=3, column=0)
    cantidad_entry = tk.Entry(ventana)
    cantidad_entry.grid(row=3, column=1)

    tk.Label(ventana, text="Precio Compra").grid(row=4, column=0)
    precio_entry = tk.Entry(ventana)
    precio_entry.grid(row=4, column=1)

    def agregar_detalle():
        detalles.append({
            "id_producto": int(producto_entry.get()),
            "cantidad": int(cantidad_entry.get()),
            "precio_compra": float(precio_entry.get())
        })
        messagebox.showinfo("Detalle", "Producto agregado")

    def registrar():
        id_proveedor = int(proveedor_entry.get())
        observacion = obs_entry.get()
        id_entrada = registrar_entrada(id_proveedor, user_data["id_usuario"], observacion, detalles)
        messagebox.showinfo("Éxito", f"Entrada registrada con ID: {id_entrada}")
        ventana.destroy()

    tk.Button(ventana, text="Agregar Producto", command=agregar_detalle).grid(row=5, column=0, pady=10)
    tk.Button(ventana, text="Registrar Entrada", command=registrar).grid(row=5, column=1, pady=10)