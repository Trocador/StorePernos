import pytest
from services.auth_service import login
from database.repositories import usuarios_repo
from utils.security import hash_password

def test_login_success(test_conn):
    usuarios_repo.create_usuario(test_conn, ("admin", hash_password("1234"), "admin", 1))
    user = login(test_conn, "admin", "1234")
    assert user is not None
    assert user["usuario"] == "admin"

def test_login_failure_wrong_password(test_conn):
    usuarios_repo.create_usuario(test_conn, ("admin", hash_password("1234"), "admin", 1))
    user = login(test_conn, "admin", "wrongpass")
    assert user is None

def test_login_failure_nonexistent_user(test_conn):
    user = login(test_conn, "ghost", "1234")
    assert user is None