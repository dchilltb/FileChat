# adapters/drive_adapter.py
from __future__ import annotations
import io, os, keyring, google.oauth2.credentials, google_auth_oauthlib.flow
from googleapiclient.discovery import build
from filechat.constants import MAX_FILE_SIZE

CREDS_SERVICE = "filechat-google"
CLIENT_SECRET_FILE = "client_secret.json"

class DriveAdapter:
    def __init__(self):
        self.creds = self._get_credentials()
        self.svc = build("drive", "v3", credentials=self.creds, cache_discovery=False)

    def _get_credentials(self):
        token = keyring.get_password(CREDS_SERVICE, "token")
        if token:
            return google.oauth2.credentials.Credentials.from_authorized_user_info(eval(token))
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE, scopes=["https://www.googleapis.com/auth/drive.readonly"]
        )
        creds = flow.run_local_server(port=0)  # browser pops up
        keyring.set_password(CREDS_SERVICE, "token", str(creds.to_json()))
        return creds

    def download(self, file_id: str) -> str:
        data = io.BytesIO()
        request = self.svc.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(data, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        if data.tell() > MAX_FILE_SIZE:
            raise ValueError("File exceeds 10 MB limit")
        return data.getvalue().decode("utf-8")
