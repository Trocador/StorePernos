from database.connection import get_connection

def test_get_connection_opens_and_closes():
    # Abre y cierra una conexión usando el context manager
    with get_connection() as conn:
        assert conn is not None
        cur = conn.execute("SELECT 1")
        assert cur.fetchone()[0] == 1