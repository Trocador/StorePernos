import os
from utils import backup

def test_backup_creates_file(tmp_path):
    # Archivo de origen
    source = tmp_path / "source.txt"
    source.write_text("contenido importante")

    # Archivo de destino
    dest = tmp_path / "backup.txt"

    backup.create_backup(str(source), str(dest))

    assert dest.exists()
    assert dest.read_text() == "contenido importante"