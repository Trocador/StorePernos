# utils/security.py
import bcrypt

# --- Hash de contraseñas ---
def hash_password(password: str) -> str:
    """Genera un hash seguro para la contraseña."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    """Verifica si la contraseña coincide con el hash almacenado."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

# --- Permisos por rol ---
def check_permission(user_role: str, required_role: str) -> bool:
    """
    Verifica si el rol del usuario tiene permisos suficientes.
    Ejemplo: admin puede hacer todo, vendedor solo ventas.
    """
    if user_role == "admin":
        return True
    return user_role == required_role