import onedrivesdk
import httplib2
import json
import os
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

        collection = self.client.item(drive="me", id=returned_item.id).children.get()

        if not collection._prop_list:
            f = open('empty.txt', 'a').close()

            self.client.item(drive="me", id=returned_item.id).children['meta1-en.txt'].upload('empty.txt')
            self.client.item(drive="me", id=returned_item.id).children['meta1-de.txt'].upload('empty.txt')
            self.client.item(drive="me", id=returned_item.id).children['meta2-en.txt'].upload('empty.txt')
            self.client.item(drive="me", id=returned_item.id).children['meta2-de.txt'].upload('empty.txt')

            os.remove('empty.txt')

        return returned_item.id

    def list_subfolders(self):

        collection = self.client.item(drive="me", id=self.main_folder).children.get()
        ret = {}

        for item in collection:
            if item.folder is not None:
               ret[item.name] = item.id

        return ret

    def download_files(self, folder_id, download_path):
        folder = self.client.item(drive="me", id=folder_id).children.get()
        i = 0
        for item in folder:
            if item.file is not None:
                self.client.item(drive="me", id=item.id).download(download_path + "/" + item.name)
                i += 1

        return True

    def get_meta_file(self, folder_name, meta_type):
        if meta_type == 1:
            name = 'meta1-en.txt'
        elif meta_type == 2:
            name = 'meta1-de.txt'
        elif meta_type == 3:
            name = 'meta2-en.txt'
        elif meta_type == 4:
            name = 'meta2-de.txt'
        else:
            return None

        if folder_name is not None:
            subfolder_id = self.create_folder(self.main_folder, folder_name)

        folder = self.client.item(drive="me", id=subfolder_id).children.get()

        for item in folder:
            if item.file is not None and item.name == name:
                self.client.item(drive="me", id=item.id).download(item.name)
                return item.id

    def update_meta_file(self, file_id, meta_type):

        if meta_type == 1:
            name = 'meta1-en.txt'
        elif meta_type == 2:
            name = 'meta1-de.txt'
        elif meta_type == 3:
            name = 'meta2-en.txt'
        elif meta_type == 4:
            name = 'meta2-de.txt'
        else:
            return None

        item = self.client.item(drive="me", id=file_id).get()
        parent_id = item.parent_reference.id

        returned_item = self.client.item(drive="me", id=parent_id).children[name].upload(name)






