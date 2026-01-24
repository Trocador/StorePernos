# ui/login_controller.py
from utils.security import verify_password

class LoginController:
    def __init__(self, conn_factory, on_success):
        self.conn_factory = conn_factory
        self.on_success = on_success

    def login(self, usuario, password):
        try:
            with self.conn_factory() as conn:
                sql = """
                SELECT id_usuario, usuario, password_hash, rol
                FROM usuarios
                WHERE usuario = ?
                """
                row = conn.execute(sql, (usuario,)).fetchone()

                if row and verify_password(password, row["password_hash"]):
                    user = {
                        "id_usuario": row["id_usuario"],
                        "usuario": row["usuario"],
                        "rol": row["rol"]
                    }
                    self.on_success(user)
                    return True
                else:
                    print("Credenciales inválidas")
                    return False
        except Exception as e:
            print("Error en login:", e)
            return False