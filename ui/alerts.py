# ui/alerts.py
from tkinter import messagebox

def info(msg, title="Información"):
    messagebox.showinfo(title, msg)

def warning(msg, title="Advertencia"):
    messagebox.showwarning(title, msg)

def error(msg, title="Error"):
    messagebox.showerror(title, msg)