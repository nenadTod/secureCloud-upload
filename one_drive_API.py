import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer


class OneDriveAPI:

    def __init__(self):
        self.client = None

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

    def upload(self, files):

        root_folder_id = self.client.item(drive="me", id="root").get().id

        print root_folder_id

        for f in files:
            k = f.rfind("\\") + 1
            returned_item = self.client.item(drive="me", id="root").children[f[k:]].upload(f)