# utils/backup_drive.py

# DummyDrive para tests
class DummyDrive:
    def upload(self, filename, content):
        self.files[filename] = content


# Función que usan los tests
def upload_to_drive(drive, filename: str, content: str):
    drive.upload(filename, content)
    return True


# Función real para subir a Google Drive
def upload_backup_to_drive():
    from utils.backup import create_backup
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.discovery import build
    from google.oauth2 import service_account

    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    SERVICE_ACCOUNT_FILE = "credentials.json"
    FOLDER_ID = "1VSeCoButEWu8P2G-OAxaDwKlKLgB6WB4"

    # Crear backup local
    backup_file = create_backup()

    # Autenticación con credenciales de servicio
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)

    # Metadatos del archivo
    file_metadata = {
        'name': backup_file.name,
        'parents': [FOLDER_ID]
    }

    # Subida del archivo
    media = MediaFileUpload(str(backup_file), mimetype='application/x-sqlite3')
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"Backup subido a Drive con ID: {uploaded_file.get('id')}")
    return uploaded_file.get('id')
