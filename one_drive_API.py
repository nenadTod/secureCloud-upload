import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer


class OneDriveAPI:

    # @property
    # def gauth(self):
    #     return self.__gauth
    #
    def __init__(self):
        return

    def upload(self, files):
        redirect_uri = "http://localhost:8080/"
        client_secret = "k84Ntgni9H86TfiDAgdaSyv"

        client = onedrivesdk.get_default_client(client_id='0000000048197E3B',
                                                scopes=['wl.signin',
                                                        'wl.offline_access',
                                                        'onedrive.readwrite'])

        auth_url = client.auth_provider.get_auth_url(redirect_uri)

        # this will block until we have the code
        code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

        client.auth_provider.authenticate(code, redirect_uri, client_secret)

        for f in files:
            k = f.rfind("\\") + 1
            returned_item = client.item(drive="me", id="root").children[f[k:]].upload(f)