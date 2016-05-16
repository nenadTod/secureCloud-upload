from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleDriveAPI:

    def __init__(self):
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = None

    def authenticate(self):
        self.drive = GoogleDrive(self.gauth)

    def upload(self, files):

        for f in files:
            k = f.rfind("\\") + 1
            file1 = self.drive.CreateFile({'title': f[k:]})
            file1.SetContentFile(f)
            file1.Upload()
