import os
import sys
from pathlib import Path

# Detectar si estamos corriendo como ejecutable (PyInstaller)
if getattr(sys, 'frozen', False):
    # Carpeta donde está el .exe
    BASE_DIR = Path(sys.executable).parent
else:
    # Carpeta base del proyecto en modo desarrollo
    BASE_DIR = Path(__file__).resolve().parent.parent

# Ruta de la base de datos SQLite
DB_PATH = BASE_DIR / "TiendaPernos.db"

# Configuración de logs
LOG_PATH = BASE_DIR / "logs"
LOG_FILE = LOG_PATH / "app.log"
os.makedirs(LOG_PATH, exist_ok=True)

# Configuración de backup (usar carpeta pública para evitar problemas de permisos)
BACKUP_DIR = Path("C:/Users/Public/TiendaPernos/backups")
os.makedirs(BACKUP_DIR, exist_ok=True)