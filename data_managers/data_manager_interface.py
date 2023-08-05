from abc import ABC, abstractmethod

# [
#   {
#     "id": 1,
#     "name": "Alice",
#     "movies": [
#       {
#         "id": 1,
#         "name": "Inception",
#         "director": "Christopher Nolan",
#         "year": 2010,
#         "rating": 8.8
#       },
#       {
#         "id": 2,
#         "name": "The Dark Knight",
#         "director": "Christopher Nolan",
#         "year": 2008,
#         "rating": 9.0
#       }
#     ]
#   },
#   {
#     "id": 2,
#     "name": "Bob",
#     "movies": []
#   }
# ]
class DataManagerInterface(ABC):
    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user(self, user_name: str, password=None, avatar_filename=None):
        pass

    @abstractmethod
    def delete_user(self, user_id: int):
        pass

    @abstractmethod
    def add_movie_to_user(self,user_id: int, movie_to_add: dict):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> dict:
        pass

    @abstractmethod
    def delete_movie_of_user(self, user_id: int, movie_id: str):
        pass

    @abstractmethod
    def get_user_movie(self, user_id: int, movie_id: str):
        pass

    @abstractmethod
    def update_movie_of_user(self, user_id: int, movie_id: str, movie_for_update: dict):
        pass

    @abstractmethod
    def get_all_public_users(self):
        pass

    @abstractmethod
    def get_all_registered_users(self):
        pass

    @abstractmethod
    def get_user_by_name(self, user_name_to_search: str):
        pass