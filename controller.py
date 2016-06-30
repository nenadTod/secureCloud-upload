import os
import tkFileDialog
import tkMessageBox
import shutil
import json
import bcrypt
import ntpath
from setuptools.command import upload_docs
from Crypto.Hash import SHA256

from download_gui import DownloadGui
from uc_register_gui import UCRegister
from cloud_API.dropbox_API import DropboxAPI
from cloud_API.one_drive_API import OneDriveAPI
from cloud_API.google_drive_API import GoogleDriveAPI
from Crypto.PublicKey import RSA
import requests
from Crypto.Cipher import AES
import binascii


from SCCrypto import SCCrypto


class Controller:

    def __init__(self, model):
        self.model=model
        self.view=""

    def switch_account_action(self):
        uc_register = UCRegister(self.view.root, self)
        print("switch account")

    def add_file_action(self):
        selected_files=[]
        options = {}
        options['filetypes'] = [('Image files', '*.jpeg *.jpg *.png *.gif *.tif *.tiff *.pcd')]
        full_files_path = tkFileDialog.askopenfilenames(**options)

        if len(full_files_path) != 0:
            files_directory = os.path.dirname(full_files_path[0])
            for full_file_path in full_files_path:
                file_name = os.path.basename(full_file_path)
                #full_file_path_formated = os.path.join(files_directory, file_name)
                full_file_path = full_file_path.replace("/", "\\")
                selected_files.append(full_file_path)
            self.model.add_files_to_list(selected_files)

    def open_download(self, selected_drive):

        if selected_drive == 'Google Drive':
            drive = GoogleDriveAPI()
        elif selected_drive == 'One Drive':
            drive = OneDriveAPI()
        else:
            drive = DropboxAPI()

        try:
            drive.authenticate()
        except:
            tkMessageBox.showinfo(title="Rejection", message="Authorization rejected by user.")

        if len(drive.list_subfolders()) == 0:
            tkMessageBox.showinfo("No Available Galleries", "You have no galleries that could be downloaded!\n"
                                                            "Please try with another account, or create gallery within this.")
        else:
            self._drive = drive
            download_view = DownloadGui(self.view.root, self, drive.list_subfolders())

    def download_action(self, folder_value):
        options = {}
        download_path = tkFileDialog.askdirectory(**options)
        end = self._drive.download_files(str(folder_value), download_path)
        if end is True:
            tkMessageBox.showinfo(title="Download success", message="Files downloaded successfully.")

    def register_user(self, email, password):
        print "pozvao je pocetak download-a " + email + " na lok " + password

    def add_folder_action(self):
        selected_files = []
        options = {}
        full_folder_path = tkFileDialog.askdirectory(**options)
        print(full_folder_path)
        for file in os.listdir(full_folder_path):
            if (file.endswith(".jpeg") or file.endswith(".jpg") or file.endswith(".png") or file.endswith(".gif") or file.endswith(".tif") or file.endswith(".tiff") or file.endswith(".pcd")):
                full_file_path = os.path.join(full_folder_path, file)
                pt = full_file_path.replace('/', '\\')
                selected_files.append(pt)
        self.model.add_files_to_list(selected_files)

    def remove_file_action(self, to_remove_index_list):
        if len(to_remove_index_list) > 0:
            self.model.remove_selected(to_remove_index_list)

    def clear_all_action(self):
        self.model.clear_files_list()

    def cancel_all_action(self):
        print("cancel")

    def start_action(self, selected_drive, encryption_type, upload_location):

        sc = SCCrypto()

        #temp_files
        temp_dir = "/sc_temp" #OVO ZAKOMENTARISI KADA BUDES SA ONIM DOLE :)
        #temp_dir = "/sc_mock" + "/sc_temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        """
        file_list = []
        for f in self.model.opened_files:
            with open(f, 'rb') as fhI:
                file_name = ntpath.split(f)[1]
                file_path = temp_dir + "/" + file_name
                pic_data = fhI.read()

                #encryption - bice zamenjene random vrendostima, naravno :)
                aes = AES.new("askldsjkuierocme", AES.MODE_CFB, 'asdfghjkqwertyui')
                enc_pic_data = aes.encrypt(pic_data)
                enc_pic_data_hex = sc.bin2hex(enc_pic_data)#ovo ti mozda i ne treba, zbog cuvanja mesta.. madaa?

                with open(file_path, 'w') as fhO:
                    fhO.write(enc_pic_data_hex)

                abs_file_path = os.path.abspath(file_path)
                file_list.append(abs_file_path)
        """
        mock_key = RSA.generate(2048)#OBAVEZNO IZBRISI OVO POSLE.
        retVal = sc.encrypt_images(temp_dir, self.model.opened_files, mock_key)
        file_list = retVal[0]
        enc_sim_key = retVal[1]
        iv_list = retVal[2]
        # mozda i abstraktna klasa? Ja bih rekao da da:P

        with open("/sc_mock/sc_temp/meta.txt", 'w') as fhO:
            fhO.write(enc_sim_key + "\n")
            i = 0
            for f in file_list:
                fhO.write(f + " " + str(iv_list[i]) + "\n")
                i += 1

        if selected_drive == 'Google Drive':
            drive = GoogleDriveAPI()
        elif selected_drive == 'One Drive':
            drive = OneDriveAPI()
        else:
            drive = DropboxAPI()

        try:
            drive.authenticate()
        except:
            tkMessageBox.showinfo(title="Rejection", message="Authorization rejected by user.")
        id = drive.get_user_data()
        drive.upload(file_list, upload_location)

        """ Komunikacija sa serverom
        hid = SHA256.new(id).hexdigest()
        print hid
        r = requests.post('http://127.0.0.1:8000/api/exist/', json={"id": hid})

        dct = json.loads(r.content)
        retVal = dct[0]['retVal']

        if retVal == "No":
            reqM = SHA256.new("nenadtod@live.com").hexdigest()
            psw = bcrypt.hashpw("hassan", bcrypt.gensalt())
            r = requests.post('http://127.0.0.1:8000/api/newE/', json={"id": hid, "psw": psw, "reqM": reqM})
        else:
            psw = "hassan"
            r = requests.post('http://127.0.0.1:8000/api/getPK/', json={"id": hid, "psw": psw})
        """


        shutil.rmtree(temp_dir)
        #sve ispod je eksperimentalnog karaktera :D

        #mock_files
        """dekripcija odradjena, ceka neka lepsa vremena :D
        mock_dir = "/sc_mock"
        mock_sc_meta1 = mock_dir + "/" + "mock_meta1.txt"


        splitted = sc.splitSK_RSA(mock_key)

        with open(mock_sc_meta1, 'w') as fhO:
                    fhO.write(splitted[0])



        mock_dir2 = "/sc_storage"
        if not os.path.exists(mock_dir2):
            os.makedirs(mock_dir2)

        sc_meta2 = "/sc_storage" + "/" + "skp.txt"
        with open(sc_meta2, 'w') as fhO:
                    fhO.write(splitted[1])

        sc_meta3 = "/sc_storage" + "/" + "pk.txt"
        with open(sc_meta3, 'w') as fhO:
                    fhO.write(mock_key.publickey().exportKey())
        #dsk = mock_key.decrypt(sc.b642bin(enc_sim_key))
        dsk = None
        with open("/sc_mock/sc_temp/meta.txt", 'r') as fhI:
            i = 1
            for line in fhI:
                line_content = str.split(line)
                if len(line_content) == 1:
                    dsk = mock_key.decrypt(sc.b642bin(line_content[0]))
                else:

                    with open(line_content[0], 'r') as fhI2:
                        enc_pic_data_hex = fhI2.read()
                        enc_pic_data_bin = sc.b642bin(enc_pic_data_hex)

                        aes2 = AES.new(dsk, AES.MODE_CFB, sc.b642bin(line_content[1]))
                        dec_pic_data_bin = aes2.decrypt(enc_pic_data_bin)

                        iStr = str(i)
                        location = mock_dir2 + "/proof" + iStr + ".png"
                        with open(location, 'wb') as fhO:
                            fhO.write(dec_pic_data_bin)
                    i += 1
        """
        self.clear_all_action()

        tkMessageBox.showinfo(title="Upload success", message="Files uploaded successfully.")

    def exit_action(self):
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            self.view.root.destroy()