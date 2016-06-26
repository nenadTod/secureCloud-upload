import tkMessageBox
import os
import tkFileDialog
import ntpath
import shutil
from google_drive_API import GoogleDriveAPI
from one_drive_API import OneDriveAPI
from dropbox_API import DropboxAPI

from Crypto.Cipher import AES
from SCCrypto import SCCrypto

class Controller:

    @property
    def model(self):
        return self.__model

    @property
    def root(self):
        return self.__root

    def __init__(self, root, model):
        self.__model=model
        self.__root=root

    def switch_account_action(self):
        print("switch account")

    def add_file_action(self):
        print("add files")
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

    def add_folder_action(self):
        print("add folder")
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
        print("remove file/files")
        if len(to_remove_index_list) > 0:
            self.model.remove_selected(to_remove_index_list)

    def clear_all_action(self):
        print("clear")
        self.model.clear_files_list()

    def cancel_all_action(self):
        print("cancel")

    def start_action(self, selectedDrive, encryption_type):

        sc = SCCrypto()

        #temp_files
        temp_dir = "/sc_temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        file_list = []

        for f in self.model.opened_files:
            with open(f, 'rb') as fhI:
                file_name = ntpath.split(f)[1]
                file_path = temp_dir + "/" + file_name
                pic_data = fhI.read()


                #encryption - bice zamenjene random vrendostima, naravno :)
                aes = AES.new("askldsjkuierocme", AES.MODE_CFB, 'asdfghjkqwertyui')
                enc_pic_data = aes.encrypt(pic_data)
                enc_pic_data_hex = sc.bin2hex(enc_pic_data)

                with open(file_path, 'w') as fhO:
                    fhO.write(enc_pic_data_hex)

                abs_file_path = os.path.abspath(file_path)
                file_list.append(abs_file_path)


        # mozda i abstraktna klasa? Ja bih rekao da da:P

        if selectedDrive == 'Google Drive':
            drive = GoogleDriveAPI()
        elif selectedDrive == 'One Drive':
            drive = OneDriveAPI()
        else:
            drive = DropboxAPI()

        drive.authenticate()
        drive.getUserData()
        drive.upload(file_list)

        """
        #proof, uncomment to se effects
        with open(file_list[0], 'r') as fhI:
            enc_pic_data_hex = fhI.read()
            enc_pic_data_bin = sc.hex2bin(enc_pic_data_hex)

            aes2 = AES.new("askldsjkuierocme", AES.MODE_CFB, 'asdfghjkqwertyui')
            dec_pic_data_bin = aes2.decrypt(enc_pic_data_bin)

            with open("/sc_temp/proof.png", 'wb') as fhO:
                fhO.write(dec_pic_data_bin)
        """

        shutil.rmtree(temp_dir)

    def exit_action(self):
        print("exit")
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            self.root.destroy()