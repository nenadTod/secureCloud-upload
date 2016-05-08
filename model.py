from gui import Gui

class Model:

    @property
    def opened_files(self):
        return self.__opened_files

    @opened_files.getter
    def opened_files(self):
        return self.__opened_files

    # @property
    # def view(self):
    #     return self.__view
    #
    # @view.setter
    # def view(self, view):
    #     self.__view = view

    view=""

    def __init__(self):
        self.view=lambda: None
        self.opened_files=[]

    def set_view(self, view):
        self.view=view

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

