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
    def upload(self, files):
        pass

    @abstractmethod
    def create_folder(self, name, folder_name):
        pass
