from data_manager_interface import DataManagerInterface
import os
import json

class JSONDataManager(DataManagerInterface):
    def __init__(self, filename: str):
        """
        Initialize the JSONDataManager class

        Args:
           filename (str): The name of the file without extension
        """
        if not isinstance(filename, str) or not filename:
            raise ValueError('Filename should be a non-empty string')

        self._data_folder = "data"
        self.file_name = filename


    @property
    def file_name(self) -> str:
        """
        Get the full path of the file

        Returns: (str) Full path of the file
        """
        return os.path.join(self._data_folder, self._file_name + ".json")

    @file_name.setter
    def file_name(self, name_of_file):
        """
        Set the filename and create an empty JSON file if it doesn't exist

        Args:
            name_of_file (str): The name of the file without extension
        """
        if not isinstance(name_of_file, str) or not name_of_file:
            raise ValueError('Filename should be a non-empty string')
        self._file_name = name_of_file
        full_path = self.file_name

        # case if there is json file with that name in self._data_folder
        if not os.path.exists(full_path):
            with open(full_path, "w") as file:
                json.dump([], file)


    def get_all_users(self) -> list:
        with open(self.file_name, 'r') as file:
            data = json.load(file)
        return data

    def get_user_movies(self, user_id):
        all_users = self.get_all_users()
        found_user = next((user for user in all_users if user['id'] == user_id), None)
        if found_user:
            return found_user['movies']



