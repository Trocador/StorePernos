import ttkbootstrap.dialogs as dialogs

def info(msg, title="Información"):
    dialogs.Messagebox.show_info(message=msg, title=title)

def warning(msg, title="Advertencia"):
    dialogs.Messagebox.show_warning(message=msg, title=title)

def error(msg, title="Error"):
    dialogs.Messagebox.show_error(message=msg, title=title)