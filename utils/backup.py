# utils/backup.py
import shutil
from datetime import datetime
from config.settings import DB_PATH, BACKUP_DIR
from pathlib import Path

def create_backup(source_path: str | Path = DB_PATH, dest_path: str | Path | None = None):
    """
    Crea una copia de seguridad del archivo source_path en dest_path.
    Si dest_path no se da, usa BACKUP_DIR con timestamp.
    """
    source_path = Path(source_path)
    if dest_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_path = BACKUP_DIR / f"inventario_{timestamp}.db"
    dest_path = Path(dest_path)
    shutil.copy(source_path, dest_path)
    return dest_path

def restore_backup(backup_file: str | Path):
    """Restaura la base desde una copia de seguridad."""
    backup_file = Path(backup_file)
    if not backup_file.exists():
        raise FileNotFoundError("El archivo de backup no existe")
    shutil.copy(backup_file, DB_PATH)
    return DB_PATH
