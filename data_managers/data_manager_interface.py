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
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user(self, use_name):
        pass

    @abstractmethod
    def delete_user(self, user_id: int):
        pass