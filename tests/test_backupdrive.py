import pytest
from utils import backup_drive

class DummyDrive:
    def __init__(self):
        self.files = {}
    def upload(self, filename, content):
        self.files[filename] = content
        return True

def test_backup_drive_upload():
    drive = DummyDrive()
    result = backup_drive.upload_to_drive(drive, "test.txt", "contenido")
    assert result is True
    assert "test.txt" in drive.files
    assert drive.files["test.txt"] == "contenido"