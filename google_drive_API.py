from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleDriveAPI:

    @property
    def gauth(self):
        return self.__gauth

    def __init__(self):
        self.__gauth = GoogleAuth()
        self.__gauth.LocalWebserverAuth()

    def upload(self, files):
        drive = GoogleDrive(self.gauth)

        for f in files:
            k = f.rfind("\\") + 1
            file1 = drive.CreateFile({'title': f[k:]})
            file1.SetContentFile(f)
            file1.Upload()
