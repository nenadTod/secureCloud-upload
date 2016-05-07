
import tkMessageBox

class Controller:

    _model=""
    _root=""

    def __init__(self, model):
        _model=model

    @staticmethod
    def switch_account_action():
        print("switch account")

    @staticmethod
    def change_location_action():
        print("change location")

    @staticmethod
    def add_file_action():
        print("add files")

    @staticmethod
    def add_folder_action():
        print("add folder")

    @staticmethod
    def remove_file_action():
        print("remove file")

    @staticmethod
    def clear_all_action():
        print("clear list")

    @staticmethod
    def cancel_all_action():
        print("cancel")

    @staticmethod
    def start_action():
        print("encript and upload")

    @staticmethod
    def exit_action(root):
        print("exit")
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            root.destroy()