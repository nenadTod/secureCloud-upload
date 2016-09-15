from gui import Gui

class Model:

    def __init__(self):
        self.opened_files = []

    def add_files_to_list(self, files_list):
        self.opened_files.extend(files_list)

    def clear_files_list(self):
        self.opened_files = []

    def remove_selected(self, to_remove_index_list):
        for to_remove_index in reversed(to_remove_index_list):
            del self.opened_files[to_remove_index]

