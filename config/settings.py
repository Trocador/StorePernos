# config/settings.py

import os
from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Ruta de la base de datos SQLite
DB_PATH = BASE_DIR / "TiendaPernos.db"

# Configuración de logs
LOG_PATH = BASE_DIR / "logs"
LOG_FILE = LOG_PATH / "app.log"

# Crear carpeta de logs si no existe
os.makedirs(LOG_PATH, exist_ok=True)

# Configuración de backup
BACKUP_DIR = BASE_DIR / "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)