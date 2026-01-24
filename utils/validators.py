# utils/validators.py

def validate_positive_number(value):
    if value <= 0:
        raise ValueError("Debe ser positivo")
    return True

def validate_positive(value):
    return validate_positive_number(value)


def validate_non_empty(value):
    if not value or not str(value).strip():
        raise ValueError("No puede estar vacío")
    return True
