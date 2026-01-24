import pytest
from utils.security import hash_password, verify_password
from utils import validators

# --- Security ---
def test_hash_and_verify_password_success():
    hashed = hash_password("secret")
    assert verify_password("secret", hashed)

def test_verify_password_failure():
    hashed = hash_password("secret")
    assert not verify_password("wrong", hashed)

# --- Validators ---
def test_validate_positive_pass():
    assert validators.validate_positive(10)

def test_validate_positive_fail():
    with pytest.raises(ValueError):
        validators.validate_positive(-5)

def test_validate_non_empty_pass():
    assert validators.validate_non_empty("hola")

def test_validate_non_empty_fail():
    with pytest.raises(ValueError):
        validators.validate_non_empty("")