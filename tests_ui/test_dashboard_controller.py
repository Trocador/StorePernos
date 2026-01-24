# tests_ui/test_dashboard_controller.py
import pytest
import sqlite3
from database import init_schema
from ui.dashboard_controller import DashboardController

class DummyConn:
    def __enter__(self): return self
    def __exit__(self, *args): pass

def conn_factory_stub():
    conn = sqlite3.connect(":memory:")
    init_schema(conn)   # crea tablas
    return conn

def test_crear_producto_success():
    msgs = {"info": None, "error": None}
    controller = DashboardController(
        conn_factory=conn_factory_stub,
        on_info=lambda m: msgs.update(info=m),
        on_error=lambda m: msgs.update(error=m)
    )
    ok = controller.crear_producto("perno", 10)
    assert ok is True
    assert msgs["info"] == "Producto creado correctamente"
    assert msgs["error"] is None

def test_crear_producto_invalid():
    msgs = {"info": None, "error": None}
    controller = DashboardController(
        conn_factory=conn_factory_stub,
        on_info=lambda m: msgs.update(info=m),
        on_error=lambda m: msgs.update(error=m)
    )
    ok = controller.crear_producto("", -5)
    assert ok is False
    assert msgs["error"] == "Tipo y stock deben ser válidos"

def test_registrar_venta_success(monkeypatch):
    msgs = {"info": None, "error": None}
    controller = DashboardController(
        conn_factory=conn_factory_stub,
        on_info=lambda m: msgs.update(info=m),
        on_error=lambda m: msgs.update(error=m)
    )

    # Stub registrar_venta
    monkeypatch.setattr(
    "ui.dashboard_controller.registrar_venta",
    lambda *a, **k: 1
)


    ok = controller.registrar_venta(1, 1, 2, 1.5)
    assert ok is True
    assert msgs["info"] == "Venta registrada correctamente"

def test_registrar_venta_error(monkeypatch):
    msgs = {"info": None, "error": None}
    controller = DashboardController(
        conn_factory=conn_factory_stub,
        on_info=lambda m: msgs.update(info=m),
        on_error=lambda m: msgs.update(error=m)
    )

    # Monkeypatch en el namespace donde se usa
    def fail(*a, **k):
        raise ValueError("Stock insuficiente")

    monkeypatch.setattr("ui.dashboard_controller.registrar_venta", fail)

    ok = controller.registrar_venta(1, 1, 5, 1.5)
    assert ok is False
    assert msgs["error"] == "Stock insuficiente"
