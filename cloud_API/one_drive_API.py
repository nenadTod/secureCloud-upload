import onedrivesdk
import httplib2
import json
from abstract_drive_API import AbstractDriveAPI
from onedrivesdk.helpers import GetAuthCodeServer


class OneDriveAPI(AbstractDriveAPI):

    def __init__(self):
        self.client = None
        self.access_token = ""
        self.main_folder = None

    def authenticate(self):

        redirect_uri = "http://localhost:8080/"
        client_secret = "k84Ntgni9H86TfiDAgdaSyv"

        self.client = onedrivesdk.get_default_client(client_id='0000000048197E3B',
                                                scopes=['wl.signin',
                                                        'wl.offline_access',
                                                        'wl.skydrive_update',
                                                        'onedrive.readwrite'])

        auth_url = self.client.auth_provider.get_auth_url(redirect_uri)

        # this will block until we have the code
        code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

        self.client.auth_provider.authenticate(code, redirect_uri, client_secret)
        self.access_token = self.client.auth_provider._session.access_token

        self.main_folder = self.create_folder("root", "Secure-Cloud")

    def get_user_data(self):
        h = httplib2.Http()
        resp, content = h.request(
            uri='https://apis.live.net/v5.0/me?access_token=' + self.access_token,
            method='GET'
        )

        data = json.loads(content)
        print data['id']
        return data['id']

    def upload(self, files, folder_name):

        if not files:
            return

        folder_id = self.main_folder

        if folder_name is not None:
            subfolder_id = self.create_folder(self.main_folder, folder_name)
            folder_id = subfolder_id

        for f in files:
            k = f.rfind("\\") + 1
            returned_item = self.client.item(drive="me", id=folder_id).children[f[k:]].upload(f)

    def create_folder(self, parent, name):

        f = onedrivesdk.Folder()
        i = onedrivesdk.Item()
        i.name = name
        i.folder = f

        returned_item = self.client.item(drive="me", id=parent).children.add(i)
        return returned_item.id

    def list_subfolders(self):

        collection = self.client.item(drive="me", id=self.main_folder).children.get()

        for item in collection:
            if item.folder is not None:
                print item.name
                print item.id

    def download_files(self, folder_id):
        folder = self.client.item(drive="me", id=folder_id).children.get()
        i = 0
        for item in folder:
            if item.file is not None:
                self.client.item(drive="me", id=item.id).download("./" + item.name)
                i += 1

