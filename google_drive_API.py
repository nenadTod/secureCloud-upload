from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import httplib2
import json


class GoogleDriveAPI:

    def __init__(self):
        self.gauth = None
        self.drive = None
        self.access_token = ""

    def authenticate(self):

        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

        self.access_token = self.gauth.credentials.access_token

    def getUserData(self):
        h = httplib2.Http()
        resp, content = h.request(
            uri='https://www.googleapis.com/drive/v2/about',
            method='GET',
            headers={'Authorization': 'Bearer ' + self.access_token}
        )

        data = json.loads(content)
        print data['user']['emailAddress']

    def upload(self, files):

        for f in files:
            k = f.rfind("\\") + 1
            file1 = self.drive.CreateFile({'title': f[k:]})
            file1.SetContentFile(f)
            file1.Upload()
