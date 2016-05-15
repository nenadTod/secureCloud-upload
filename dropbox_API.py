import dropbox
import webbrowser
import tkSimpleDialog

class DropboxAPI:

    def __init__(self):
        return

    def upload(self, files):

        app_key = '8fpo1be2toxz06w'
        app_secret = '70ruabr9bbn4eq4'

        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

        authorize_url = flow.start()

        webbrowser.open_new(authorize_url)

        code = tkSimpleDialog.askstring("Code prompt", "Enter your Dropbox code")

        if (code == None):
            return

        access_token, user_id = flow.finish(code)

        client = dropbox.client.DropboxClient(access_token)

        for f in files:
            dropbox_file = open(f, 'rb')
            k = f.rfind("\\") + 1
            client.put_file(f[k:], dropbox_file)
