import os.path
import pickle

import file_handler
import credentials

class _UserDataManager:
    _user_data = None
    _instance = None

    def reset_user_data(self):
        self._user_data = {
            "root_folder": None,
            "last_upload_local_path": None,
            "last_upload_gdrive_path": None,
            "last_upload_gdrive_file": None,
        }

    def is_initialized(self):
        return not self._user_data == None

    def init_user_data(self):
        if os.path.exists('user_data.pickle'):
            with open('user_data.pickle', 'rb') as data:
                self._user_data = pickle.load(data)
        else:
            self.reset_user_data()
            self.save_user_data()

    def save_user_data(self):
        with open('user_data.pickle', 'wb') as data:
            pickle.dump(self._user_data, data)

    def get_root_folder_id(self):
        if self._user_data["root_folder"] == None:
            self._user_data["root_folder"] = file_handler.get_gdrive_file("root")
            self.save_user_data()
        return self._user_data["root_folder"]

    def set_last_upload_local_path(self, path):
        if os.path.exists(path):
            self._user_data['last_upload_local_path'] = path
            self.save_user_data()

    def get_last_upload_local_path(self):
        return self._user_data['last_upload_local_path']

    def set_last_upload_gdrive_path(self, path):
        self._user_data['last_upload_gdrive_path'] = path
        self.save_user_data()

    def get_last_upload_gdrive_path(self):
        return self._user_data['last_upload_gdrive_path']
        
    def set_last_upload_gdrive_file(self, file):
        self._user_data['last_upload_gdrive_file'] = file
        self.save_user_data()

    def get_last_upload_gdrive_file(self):
        return self._user_data['last_upload_gdrive_file']

def UserDataManager():
    if _UserDataManager._instance == None:
        _UserDataManager._instance = _UserDataManager()
    return _UserDataManager._instance