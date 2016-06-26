import onedrivesdk
import httplib2
import json
from onedrivesdk.helpers import GetAuthCodeServer


class OneDriveAPI:

    def __init__(self):
        self.client = None
        self.access_token = ""

    def authenticate(self):

        redirect_uri = "http://localhost:8080/"
        client_secret = "k84Ntgni9H86TfiDAgdaSyv"

        self.client = onedrivesdk.get_default_client(client_id='0000000048197E3B',
                                                scopes=['wl.signin',
                                                        'wl.offline_access',
                                                        'onedrive.readwrite'])

        auth_url = self.client.auth_provider.get_auth_url(redirect_uri)

        # this will block until we have the code
        code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

        self.client.auth_provider.authenticate(code, redirect_uri, client_secret)
        self.access_token = self.client.auth_provider._session.access_token


    def getUserData(self):
        h = httplib2.Http()
        resp, content = h.request(
            uri='https://apis.live.net/v5.0/me?access_token=' + self.access_token,
            method='GET'
        )

        data = json.loads(content)
        print data['id']

    def upload(self, files):

        root_folder_id = self.client.item(drive="me", id="root").get().id

        print root_folder_id

        for f in files:
            k = f.rfind("\\") + 1
            returned_item = self.client.item(drive="me", id="root").children[f[k:]].upload(f)