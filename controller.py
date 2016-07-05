import os
import tkFileDialog
import tkMessageBox

from gui_download import DownloadGui
from cloud_API.dropbox_API import DropboxAPI
from cloud_API.one_drive_API import OneDriveAPI
from cloud_API.google_drive_API import GoogleDriveAPI
from SCCrytpo_API.SCEncryptor import SCEncryptor
from SCCrytpo_API.SCDecryptor import SCDecryptor
from gui_uc_register import UCRegister
from messages import Msg


class Controller:

    def __init__(self, model):
        self.model=model
        self.view=""

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
            tkMessageBox.showinfo(Msg.connection_rejected_title, Msg.connection_rejected_message)

        if len(drive.list_subfolders()) == 0:
            tkMessageBox.showinfo(Msg.galleries_no_available_title, Msg.galleries_no_available_message)
        else:
            self._drive = drive
            DownloadGui(self.view.root, self, drive.list_subfolders())

    def download_action(self, folder_value, folder_name, download_path):
        scd = SCDecryptor()
        end = scd.decryptLocal(str(folder_value), folder_name, download_path, self._drive)

        if end is True:
            tkMessageBox.showinfo(Msg.download_success_title, Msg.download_success_message)

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
            tkMessageBox.showinfo(Msg.connection_rejected_title, Msg.connection_rejected_message)
            return

        sce = SCEncryptor(self)
        if encryption_type == 1:
            success = sce.encryptLocal(self.model.opened_files, drive, upload_location)
        else:
            success = sce.encryptShared(self.model.opened_files, drive, upload_location)

        self.clear_all_action()

        if success:
            tkMessageBox.showinfo(Msg.upload_success_title, Msg.upload_success_message)


    def add_file_action(self):
        selected_files = []
        options = {}
        options['filetypes'] = [('Image files', '*.jpeg *.jpg *.png *.gif *.tif *.tiff *.pcd')]
        full_files_path = tkFileDialog.askopenfilenames(**options)

        if len(full_files_path) != 0:
            files_directory = os.path.dirname(full_files_path[0])
            for full_file_path in full_files_path:
                file_name = os.path.basename(full_file_path)
                # full_file_path_formated = os.path.join(files_directory, file_name)
                full_file_path = full_file_path.replace("/", "\\")
                selected_files.append(full_file_path)
            self.model.add_files_to_list(selected_files)

    def add_folder_action(self):
        selected_files = []
        options = {}
        full_folder_path = tkFileDialog.askdirectory(**options)
        print(full_folder_path)
        for file in os.listdir(full_folder_path):
            if (file.endswith(".jpeg") or file.endswith(".jpg") or file.endswith(".png") or file.endswith(
                    ".gif") or file.endswith(".tif") or file.endswith(".tiff") or file.endswith(".pcd")):
                full_file_path = os.path.join(full_folder_path, file)
                pt = full_file_path.replace('/', '\\')
                selected_files.append(pt)
        self.model.add_files_to_list(selected_files)

    def remove_file_action(self, to_remove_index_list):
        if len(to_remove_index_list) > 0:
            self.model.remove_selected(to_remove_index_list)

    def clear_all_action(self):
        self.model.clear_files_list()