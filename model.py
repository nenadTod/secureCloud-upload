from gui import Gui

class Model:

    def __init__(self):
        self.view = lambda: None
        self.opened_files = []

    def add_files_to_list(self, files_list):
        self.opened_files.extend(files_list)
        self.view.update_list()

    def clear_files_list(self):
        self.opened_files = []
        self.view.update_list()

    def remove_selected(self, to_remove_index_list):
        for to_remove_index in reversed(to_remove_index_list):
            del self.opened_files[to_remove_index]
        self.view.update_list()

