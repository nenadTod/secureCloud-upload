import tkMessageBox
import os
import tkFileDialog
from google_drive_API import GoogleDriveAPI
from one_drive_API import  OneDriveAPI
from dropbox_API import DropboxAPI


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

    def change_drive(self, drive):
        print("change location to ", drive)

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
        for path, subdirs, files in os.walk(full_folder_path):
            for file in files:
                if (file.endswith(".jpeg") or file.endswith(".jpg") or file.endswith(".png") or file.endswith(".gif") or file.endswith(".tif") or file.endswith(".tiff") or file.endswith(".pcd")):
                    full_file_path = os.path.join(path, file)
                    pt = full_file_path.replace('/', '\\')
                    selected_files.append(pt)
                    print(path)
        self.model.add_files_to_list(selected_files)

    def remove_file_action(self, to_remove_index_list):
        print("remove file")
        self.model.remove_selected(to_remove_index_list)

    def clear_all_action(self):
        print("clear")
        self.model.clear_files_list()

    def cancel_all_action(self):
        print("cancel")

    def start_action(self):
        # tu if-ovi u zavisnosti od selektovanog drajva?
        # mozda i abstraktna klasa?

        drive = GoogleDriveAPI()
        # drive = OneDriveAPI()
        # drive = DropboxAPI()

        drive.authenticate()
        drive.upload(self.model.opened_files)



    def exit_action(self):
        print("exit")
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            self.root.destroy()