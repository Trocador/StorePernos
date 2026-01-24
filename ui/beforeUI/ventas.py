# ui/ventas.py
import tkinter as tk
from tkinter import messagebox
from services.ventas_service import registrar_venta

def ventas_ui(user_data):
    ventana = tk.Toplevel()
    ventana.title("Registrar Venta")

    detalles = []

    tk.Label(ventana, text="ID Producto").grid(row=0, column=0)
    id_producto_entry = tk.Entry(ventana)
    id_producto_entry.grid(row=0, column=1)

    tk.Label(ventana, text="Cantidad").grid(row=1, column=0)
    cantidad_entry = tk.Entry(ventana)
    cantidad_entry.grid(row=1, column=1)

    tk.Label(ventana, text="Precio Unitario").grid(row=2, column=0)
    precio_entry = tk.Entry(ventana)
    precio_entry.grid(row=2, column=1)

    def agregar_detalle():
        detalles.append({
            "id_producto": int(id_producto_entry.get()),
            "cantidad": int(cantidad_entry.get()),
            "precio_unitario": float(precio_entry.get())
        })
        messagebox.showinfo("Detalle", "Producto agregado")

    def registrar():
        try:
            id_venta = registrar_venta(user_data["id_usuario"], detalles)
            messagebox.showinfo("Éxito", f"Venta registrada con ID: {id_venta}")
            ventana.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    tk.Button(ventana, text="Agregar Producto", command=agregar_detalle).grid(row=3, column=0, pady=10)
    tk.Button(ventana, text="Registrar Venta", command=registrar).grid(row=3, column=1, pady=10)