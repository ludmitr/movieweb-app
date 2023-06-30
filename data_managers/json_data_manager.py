from .data_manager_interface import DataManagerInterface
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
        """Loads users data from json file"""
        with open(self.file_name, 'r') as file:
            data = json.load(file)
        return data

    def get_user_movies(self, user_id):
        """Will return list with movies if user id found. otherwise None"""
        all_users = self.get_all_users()
        found_user = next((user for user in all_users if user['id'] == user_id), None)
        if found_user:
            return found_user['movies']


    def add_user(self, new_user_name: str):
        """Adding user to the json file db. User name must be a string and not empty"""
        if not isinstance(new_user_name, str):
            raise TypeError("User name need to be a string")
        if not new_user_name:
            raise ValueError("User name cannot be empty name")
        users = self.get_all_users()
        unique_id = self._get_unique_user_id(users)
        new_user = {
            "id": unique_id,
            "name": new_user_name,
            "movies": []
        }
        users.append(new_user)
        self._save_data(users)


    def delete_user(self, user_id:int):
        users = self.get_all_users()
        user_to_delete = next((user for user in users if user['id'] == user_id), None)
        if user_to_delete:
            users.remove(user_to_delete)

        self._save_data(users)

    def add_movie_to_user(self, user_id: int, movie_to_add: dict):
        """
        Adds a new movie to a user's movie list if it doesn't exist.
        Raises a UserNotFoundError if the user with passed id does not exist.
        """
        users = self.get_all_users()

        # getting user by user_id
        user = next((user for user in users if user['id'] == user_id), None)

        # If user not found, raise UserNotFoundError
        if user is None:
            raise UserNotFoundError(f"User with ID {user_id} not found")

        # looking for movie with same id
        movie_with_same_id = next((movie for movie in user["movies"]
                                   if movie['id'] == movie_to_add['id']), None)

        # adding movie if user doesn't have it in
        if not movie_with_same_id:
            user["movies"].append(
                movie_to_add)  # append to existing movie list

        self._save_data(users)

    def _save_data(self, users):
        """Saves the users data to a file in JSON format"""
        with open(self.file_name, "w") as file:
            json.dump(users, file)

    def _get_unique_user_id(self, users: list) -> int:
        """finds maximum id number, adds to it 1 and return the value"""
        if not users:
            return 1
        unique_id = (max(users, key=lambda user: user['id']))['id'] + 1

        return unique_id

    def get_user_by_id(self, user_id: int) -> dict:
        users = self.get_all_users()
        found_user = next((user for user in users if user['id'] == user_id), None)
        if found_user:
            return found_user

class UserNotFoundError(Exception):
    pass