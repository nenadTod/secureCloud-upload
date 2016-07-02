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
from SCEncryptor import SCEncryptor
from SCDecryptor import SCDecryptor
from Crypto.PublicKey import RSA
import requests
from Crypto.Cipher import AES
import binascii


from SCCryptoUtil import SCCrypto


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

    def download_action(self, folder_value, download_path):
        scd = SCDecryptor()
        end = scd.decryptLocal(str(folder_value), download_path, self._drive)

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
            return

        sce = SCEncryptor()
        sce.encryptLocal(self.model.opened_files, drive, upload_location)

        self.clear_all_action()

        tkMessageBox.showinfo(title="Upload success", message="Files uploaded successfully.")

    def exit_action(self):
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            self.view.root.destroy()