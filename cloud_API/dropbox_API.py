import dropbox
import webbrowser
import tkSimpleDialog
from abstract_drive_API import AbstractDriveAPI


class DropboxAPI(AbstractDriveAPI):

    def __init__(self):
        self.client = None

    def authenticate(self):

        app_key = '8fpo1be2toxz06w'
        app_secret = '70ruabr9bbn4eq4'

        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

        authorize_url = flow.start()

        webbrowser.open_new(authorize_url)

        code = tkSimpleDialog.askstring("Code prompt", "Enter your Dropbox code")

        if code is None:
            return

        access_token, user_id = flow.finish(code)

        self.client = dropbox.client.DropboxClient(access_token)

    def get_user_data(self):
        acc = self.client.account_info()

        email = acc['email']
        print email
        return email

    def upload(self, files, folder_name):
        if not files:
            return

        if self.client is None:
            return

        destination = '/Secure-Upload/'

        if folder_name is not None:
            destination = destination + folder_name + '/'

        for f in files:
            dropbox_file = open(f, 'rb')
            k = f.rfind("\\") + 1
            self.client.put_file(destination + f[k:], dropbox_file)

    def create_folder(self, name):
        pass
