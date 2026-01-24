from database.repositories import usuarios_repo
from utils.security import hash_password, verify_password
from tests.fixtures import usuario_base

def test_create_and_login_usuario(test_conn):
    id_usuario = usuario_base(test_conn)
    user = usuarios_repo.get_usuario(test_conn, "admin")
    assert verify_password("1234", user["password_hash"])
    assert user["rol"] == "admin"