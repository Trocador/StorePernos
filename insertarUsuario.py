from database.connection import get_connection
from database.repositories import usuarios_repo
from utils.security import hash_password

with get_connection() as conn:
    usuarios_repo.create_usuario(
        conn,
        ("admin", hash_password("1234"), "admin", 1)
    )