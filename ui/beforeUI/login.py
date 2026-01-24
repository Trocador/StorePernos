# ui/reportes.py
from database.connection import get_connection
from database.repositories import ventas_repo, movimientos_repo

def reportes_ui(user_data):
    print("\n=== REPORTES ===")
    print("1. Ventas por fecha")
    print("2. Movimientos por producto")

    opcion = input("Seleccione opción: ")

    with get_connection() as conn:
        if opcion == "1":
            inicio = input("Fecha inicio (YYYY-MM-DD): ")
            fin = input("Fecha fin (YYYY-MM-DD): ")
            ventas = ventas_repo.get_ventas_by_fecha(conn, inicio, fin)
            for v in ventas:
                print(dict(v))
        elif opcion == "2":
            id_producto = int(input("ID producto: "))
            movimientos = movimientos_repo.get_movimientos_by_producto(conn, id_producto)
            for m in movimientos:
                print(dict(m))