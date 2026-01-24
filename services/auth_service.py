# services/auth_service.py

from utils.security import verify_password
from database.repositories import usuarios_repo

def login(conn, usuario, password):
    user = usuarios_repo.get_usuario(conn, usuario)

    if not user:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    return user
