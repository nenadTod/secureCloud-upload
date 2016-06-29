import onedrivesdk
import httplib2
import json
from abstract_drive_API import AbstractDriveAPI
from onedrivesdk.helpers import GetAuthCodeServer


class OneDriveAPI(AbstractDriveAPI):

    def __init__(self):
        self.client = None
        self.access_token = ""

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

        folder_id = self.create_folder('Secure-Cloud')

        if folder_id is None:
            root_folder = self.client.item(drive="me", id="root").children.get()
            for rf in root_folder:
                if rf.name == 'Secure-Cloud':
                    folder_id = rf.id

        for f in files:
            k = f.rfind("\\") + 1
            returned_item = self.client.item(drive="me", id=folder_id).children[f[k:]].upload(f)

    def create_folder(self, parent, name):
        try:
            h = httplib2.Http()
            bodyData = {
                "name": name
            }
            bodyData = json.dumps(bodyData)
            resp, content = h.request(
                uri='https://apis.live.net/v5.0/me/skydrive',
                method='POST',
                headers={'Authorization': 'Bearer ' + self.access_token, 'Content-Type': 'application/json'},
                body=bodyData
            )
            data = json.loads(content)
            data_id = data['id'].split('.')[-1]
            return data_id
        except:
            return None
