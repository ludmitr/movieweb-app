import config
from .data_manager_interface import DataManagerInterface
from .data_models_for_sql import Movie, User, user_movie_association, db

AVATAR_DEFAULT_NAME = 'avatar_default.png'

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, name_of_db, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = config.get_absolute_db_uri(name_of_db)

    def get_all_users(self):
        """
        Returns all users data from db.
        Returned data is a LIST of users where each user is a DICT
        [{'id':1, 'name': 'Bob', movies:[{}{}]}, {}, {}...]
        user
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

        """
        users = db.session.execute(db.select(User).order_by(User.username)).scalars()

        # Transforming database records into a structured data format for app usage
        users_for_return = []
        for user in users:
            new_user = {
                'id': user.id,
                'name': user.name,
                'movies': [{
                    'id': movie.id,
                    'name': movie.name,
                    'director': movie.director,
                    'year': movie.year,
                    'rating': movie.rating,
                    'imdb_link': movie.imdb_link,
                    'image_link': movie.image_link
                } for movie in user.movies]
            }

            # Check if password is not None and then add password and avatar to new_user
            if user.password:
                new_user['password'] = user.password
                new_user['avatar'] = user.avatar

            users_for_return.append(new_user)

        return users_for_return

    def get_user_movies(self, user_id):
        """return list of movies(dict) if user id found. otherwise None"""
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one()

        if user:
            user_movies_to_return = [{
                'id': movie.id,
                'name': movie.name,
                'director': movie.director,
                'year': movie.year,
                'rating': movie.rating,
                'imdb_link': movie.imdb_link,
                'image_link': movie.image_link
            } for movie in user.movies]

            return user_movies_to_return

    def add_user(self, new_user_name: str, password=None, avatar_filename=None):
        """
        Adds a user to the sqlite db. User name must be a string and not empty.
        Passwords are hashed and salted before being stored.
        """
        # validate passed arguments
        if not isinstance(new_user_name, str):
            raise TypeError("User name need to be a string")
        if not new_user_name:
            raise ValueError("User name cannot be empty name")
        if password and len(password) < 6:
            raise ValueError("Password length must be at least 6 characters")
        user = db.session.execute(db.select(User).filter_by(named=new_user_name)).scalar_one()
        if user:
            raise ValueError(
                f"User name '{new_user_name}' already exists. Please choose a different name.")

        # creating new User to be added
        new_user = User(name=new_user_name)
        if password is not None:
            new_user.password = password
            new_user.avatar = AVATAR_DEFAULT_NAME

        db.session.add(new_user)
        db.session.commit()

    def delete_user(self, user_id: int):
        pass

    def add_movie_to_user(self, user_id: int, movie_to_add: dict):
        pass

    def get_user_by_id(self, user_id: int) -> dict:
        pass

    def delete_movie_of_user(self, user_id: int, movie_id: str):
        pass

    def get_user_movie(self, user_id: int, movie_id: str):
        pass

    def update_movie_of_user(self, user_id: int, movie_id: str,
                             movie_for_update: dict):
        pass

    def get_all_public_users(self):
        users = db.session.execute(db.select(User).filter_by(id=None)).scalars()

        users_for_return = []
        for user in users:
            new_user = {
                'id': user.id,
                'name': user.name,
            }
            users_for_return.append(new_user)
        return users_for_return

    def get_all_registered_users(self):
        pass

    def get_user_by_name(self, user_name_to_search: str):
        pass
