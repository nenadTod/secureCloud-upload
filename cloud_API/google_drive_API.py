from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import httplib2
import json
from abstract_drive_API import AbstractDriveAPI


class GoogleDriveAPI(AbstractDriveAPI):

    def __init__(self):
        self.gauth = None
        self.drive = None
        self.access_token = ""
        self.main_folder = None

    def authenticate(self):

        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

        self.access_token = self.gauth.credentials.access_token
        self._authentication_main_folder()

    def get_user_data(self):
        h = httplib2.Http()
        resp, content = h.request(
            uri='https://www.googleapis.com/drive/v2/about',
            method='GET',
            headers={'Authorization': 'Bearer ' + self.access_token}
        )

        data = json.loads(content)
        return data['user']['emailAddress']

    def upload(self, files, folder_name):

        if not files:
            return

        h = httplib2.Http()
        folder_id = self.main_folder
        subfolder_id = None

        #provera subfoldera
        if folder_name is not None:
            resp, content = h.request(
                uri='https://www.googleapis.com/drive/v2/files?q=title+%3d+%27' + folder_name + '%27',
                method='GET',
                headers={'Authorization': 'Bearer ' + self.access_token}
            )

            data = json.loads(content)

            if not data['items']:
                subfolder_id = self.create_folder(folder_id, folder_name)
            else:
                for d in data['items']:
                    if d['mimeType'] == 'application/vnd.google-apps.folder' and not d['explicitlyTrashed']:
                        subfolder_id = d['id']

                if subfolder_id is None:
                    subfolder_id = self.create_folder(folder_id, folder_name)

        if subfolder_id is not None:
            folder_id = subfolder_id

        for f in files:
            k = f.rfind("\\") + 1
            file1 = self.drive.CreateFile({'title': f[k:], "parents": [{"kind": "drive#fileLink", "id": folder_id}]})
            file1.SetContentFile(f)
            file1.Upload()

    def create_folder(self, parent_id="root", name="Secure-Cloud"):
        hf = httplib2.Http()
        bodyData = {
                "title": name,
                "parents": [{"id": parent_id}],
                "mimeType": "application/vnd.google-apps.folder"
            }
        bodyData = json.dumps(bodyData)
        resp, content = hf.request(
            uri='https://www.googleapis.com/drive/v2/files',
            method='POST',
            headers={'Authorization': 'Bearer ' + self.access_token, 'Content-Type': 'application/json'},
            body=bodyData
        )
        data = json.loads(content)
        return data['id']

    def list_subfolders(self):
        folder_id = self.main_folder
        ret = {}
        file_list = self.drive.ListFile({'q': "'" + str(
            folder_id) + "' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
        for file1 in file_list:
            ret[file1['title']] = file1['id']

        return ret

    def download_files(self, folder_id, download_path):

        file_list = self.drive.ListFile({'q': "'" + str(
            folder_id) + "' in parents and trashed=false"}).GetList()

        for file1 in file_list:
            file2 = self.drive.CreateFile({'id': file1['id']})
            file2.GetContentFile(download_path + '/' + file1['title'])

    def _authentication_main_folder(self):

        h = httplib2.Http()
        resp, content = h.request(
            uri='https://www.googleapis.com/drive/v2/files?q=title+%3d+%27Secure-Cloud%27',
            method='GET',
            headers={'Authorization': 'Bearer ' + self.access_token}
        )

        data = json.loads(content)
        folder_id = None

        if not data['items']:
            folder_id = self.create_folder()
        else:
            for d in data['items']:
                if d['mimeType'] == 'application/vnd.google-apps.folder' and not d['explicitlyTrashed']:
                    folder_id = d['id']

            if folder_id is None:
                folder_id = self.create_folder()

        self.main_folder = folder_id
