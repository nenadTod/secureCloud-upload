from abc import ABCMeta, abstractmethod


class AbstractDriveAPI(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def get_user_data(self):
        pass

    @abstractmethod
    def upload(self, files, folder_name):
        pass

    @abstractmethod
    def create_folder(self, name, folder_name):
        pass

    @abstractmethod
    def list_subfolders(self):
        pass

    @abstractmethod
    def download_files(self, folder_id, download_path):
        pass

    @abstractmethod
    def download_file(self, folder_id, file_name, download_path):
        pass

    @abstractmethod
    def download_shared_file(self, folder_id, file_name, download_path):
        pass

    @abstractmethod
    def get_user_id_by_folder_id(self, folder_id):
        pass

    @abstractmethod
    def get_meta_file(self, folder_name, save_to_folder, meta_type):
        pass

    @abstractmethod
    def update_meta_file(self, file_id, from_folder, meta_type):
        pass
