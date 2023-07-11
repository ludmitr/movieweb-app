from .data_manager_interface import DataManagerInterface
import os
import json
import bcrypt

AVATAR_FILE_NAMES = {
    'default': 'avatar_default.png'
}
class JSONDataManager(DataManagerInterface):
    """
    This class manages a list of users and their movies. Each user is represented
    as a dictionary with the following structure:

    {
        "id": <unique id of user, an integer>,
        "name": <name of user, a string>,
        "movies": [<list of movies, each movie is a dictionary>]
    }

    Each movie in the 'movies' list is represented as a dictionary with the
    following structure:

    {
        "id": <unique id of movie, a string>,
        "title": <title of movie, a string>,
        "year": <year of movie, an integer>,
        ...
        <additional movie properties>
    }

    The list of users is stored in a JSON file.
    """

    def __init__(self, filename: str):
        if not isinstance(filename, str) or not filename:
            raise ValueError('Filename should be a non-empty string')

        self._data_folder = "data"
        self.file_name = filename

    @property
    def file_name(self) -> str:
        """Get the full path of the file"""
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
        found_user = next(
            (user for user in all_users if user['id'] == user_id), None)
        if found_user:
            return found_user['movies']

    def add_user(self, new_user_name: str, password=None, avatar_filename=None):
        """
        Adds a user to the json file db. User name must be a string and not empty.
        Passwords are hashed and salted before being stored.
        """
        # validate passed arguments
        if not isinstance(new_user_name, str):
            raise TypeError("User name need to be a string")
        if not new_user_name:
            raise ValueError("User name cannot be empty name")
        if password and len(password) < 6:
            raise ValueError("Password length must be at least 6 characters")

        users = self.get_all_users()
        # Check if the user name already exists
        for user in users:
            if user['name'] == new_user_name:
                raise ValueError(
                    f"User name '{new_user_name}' already exists. Please choose a different name.")

        # creating new_user dict to be added
        new_user = {
            "id": self._get_unique_user_id(users),
            "name": new_user_name,
            "movies": []
        }
        # adding password and avatar to the new_user dict
        if password:
            new_user["password"] = self._encode_hash_and_decode_password(password)
            if avatar_filename is None or avatar_filename not in os.listdir(
                    'static/images'):
                avatar_filename = AVATAR_FILE_NAMES['default']
            new_user["avatar"] = avatar_filename

        users.append(new_user)
        self._save_data(users)

    def delete_user(self, user_id: int):
        all_users = self.get_all_users()

        # finding user by id and if it found - deleting it
        user_to_delete = next(
            (user for user in all_users if user['id'] == user_id), None)
        if user_to_delete:
            all_users.remove(user_to_delete)
            self._save_data(all_users)

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
            user["movies"].append(movie_to_add)

        self._save_data(users)

    def delete_movie_of_user(self, user_id: int, movie_id: str):
        """Removes a specific movie from a user's movie list based on provided user_id and movie_id."""
        users = self.get_all_users()

        # finding user and movie by id, and deleting movie. save data if movie deleted
        user = next((user for user in users if user['id'] == user_id), None)
        if user is None:
            raise ValueError(f"User with id {user_id} does not exist")

        movies_of_user: list = user['movies']
        movie_to_delete = next(
            (movie for movie in movies_of_user if movie['id'] == movie_id),
            None)

        if movie_to_delete is None:
            raise ValueError(
                f"Movie with id {movie_id} does not exist for user {user_id}")

        movies_of_user.remove(movie_to_delete)
        self._save_data(users)

    def get_user_movie(self, user_id: int, movie_id: str):
        """Get the user's specific movie by its ID. return None if user or movies
        with that id doesn't exist"""
        user = self.get_user_by_id(user_id)
        if user:
            found_movie = next((movie for movie in user['movies']
                                if movie_id == movie['id']), None)
            if found_movie:
                return found_movie

    def get_user_by_id(self, user_id: int) -> dict:
        """Retrieves a user's information based on the provided user_id.
        Returns None if there is no user with that id"""
        users = self.get_all_users()
        found_user = next((user for user in users if user['id'] == user_id),
                          None)
        if found_user:
            return found_user

    def update_movie_of_user(self, user_id: int, movie_id: str,
                             movie_data_to_update: dict):
        """
        This method is used to update a specific movie of a specific user
        based on the user_id and movie_id provided.
        """
        all_users = self.get_all_users()
        # Find the user whose movie we want to update
        user = next((user for user in all_users if user['id'] == user_id),
                    None)

        if not user:
            raise ValueError(f"No user found with ID {user_id}")

        # Find the movie we want to update
        movie: dict = next(
            (movie for movie in user['movies'] if movie['id'] == movie_id),
            None)

        # If the movie doesn't exist - raise an error
        if not movie:
            raise ValueError(
                f"No movie found with ID {movie_id} for user {user_id}")

        # If the movie exists - update
        movie.update(movie_data_to_update)

        # Save all user data back to file.
        self._save_data(all_users)

    def get_all_public_users(self):
        """Returns a list of all public users. Public users are those who don't have a password."""
        all_users = self.get_all_users()
        return [user for user in all_users if 'password' not in user]

    def get_all_registered_users(self):
        """Returns a list of all registered users. Registered users are those who have a password."""
        all_users = self.get_all_users()
        return [user for user in all_users if 'password' in user]

        """Check a user's password."""
        user = self.get_user_by_name(user_name)
        if user and 'password' in user:
            stored_password_hash = user['password'].encode(
                'utf-8')  # get the stored password hash
            password_to_check_hash = bcrypt.hashpw(
                password_to_check.encode('utf-8'), stored_password_hash)
            return stored_password_hash == password_to_check_hash

        return False  # return False for users without a password, or if the user doesn't exist

    def is_password_valid(self, user_name: str, password_to_check: str) -> bool:
        """
           Checks the validity of a user's password by comparing a provided
           password with the stored hash of the user's actual password.
        """
        all_users = self.get_all_users()
        user_name_matched = next((user for user in all_users if user['name'] == user_name), None)
        # checking if stored password of user match the password_to_check
        if user_name_matched and 'password' in user_name_matched:
            stored_password_hash = user_name_matched['password'].encode('utf-8')
            password_to_check_hash = bcrypt.hashpw(password_to_check.encode('utf-8'),
                                                   stored_password_hash)

            return stored_password_hash == password_to_check_hash

        return False  # return False for users without a password, or if the user doesn't exist

    def get_user_by_name(self, user_name_to_search: str):
        """Return user: dict with the same name. if not found returns None"""
        all_reg_users = self.get_all_users()
        return next((user for user in all_reg_users if user['name'] == user_name_to_search), None)

    # -------------- inner logic methods--------------------------------

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

    def _encode_hash_and_decode_password(self, password: str) -> str:
        """Encodes, hashes, and decodes a given password using bcrypt."""
        password_hash = bcrypt.hashpw(password.encode('utf-8'),
                                      bcrypt.gensalt())
        return password_hash.decode('utf-8')

class UserNotFoundError(Exception):
    pass
