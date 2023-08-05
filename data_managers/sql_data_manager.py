import config
from .data_manager_interface import DataManagerInterface
from .data_models_for_sql import Movie, User, db
import bcrypt
from datetime import datetime

AVATAR_DEFAULT_NAME = 'avatar_default.png'


class SQLiteDataManager(DataManagerInterface):
    ENCODING_TYPE = 'utf-8'

    def __init__(self, name_of_db, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = config.get_absolute_db_uri(name_of_db)

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
        user = db.session.execute(
            db.select(User).filter_by(name=new_user_name)).scalar_one_or_none()
        if user:
            raise ValueError(
                f"User name '{new_user_name}' already exists. Please choose a different name.")

        # creating new User to be added
        new_user = User(name=new_user_name)
        if password is not None:
            new_user.password = self._hash_and_encode_password(password)
            new_user.avatar = AVATAR_DEFAULT_NAME

        db.session.add(new_user)
        db.session.commit()

    def delete_user(self, user_id: int):
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
        if not user:
            raise ValueError(f"User with that id: {user_id} doesnt exist.")

        # running on user movies and deleting movie if it's not associated with other movies
        for movie in user.movies:
            if len(movie.users) == 1:
                db.session.delete(movie)

        db.session.delete(user)
        db.session.commit()

    def add_movie_to_user(self, user_id: int, movie_data: dict):
        """if the movies doesnt exist in db - adds a new movie and associate it with user."""
        # checking if the movie exist in db, if not - adding it to db.
        movie = db.session.execute(
            db.select(Movie).filter_by(id=movie_data['id'])).scalar_one_or_none()
        if not movie:
            movie = Movie(id=movie_data['id'], name=movie_data['name'],
                          director=movie_data['director'], year=movie_data['year'],
                          rating=movie_data['rating'], imdb_link=movie_data['imdb_link'],
                          image_link=movie_data['image_link']
                          )
            db.session.add(movie)
            db.session.commit()

        # adding relation to user_movie_association
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
        if user:
            movie.users.append(user)
            db.session.commit()

    def get_user_by_id(self, user_id: int) -> dict:
        """
        Retrieves a user's data based on the provided user_id.
        Returns None if there is no user with that id
        """
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()

        if user:
            user_to_return = {
                'id': user.id,
                'name': user.name,
                'movies': [self._fetch_movie_data(movie) for movie in user.movies]
            }

            return user_to_return

    def delete_movie_of_user(self, user_id: int, movie_id: str):
        # getting movie and user instances
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
        movie = db.session.execute(db.select(Movie).filter_by(id=movie_id)).scalar_one_or_none()

        # data validation
        if not user:
            raise ValueError(f"User with that id: {user_id} doesnt exist.")
        if not movie:
            raise ValueError(f"Movie with that id: {movie_id} doesnt exist.")

        # removing the movie from user.movies and if the movies doesnt have any users associated, remove the movie too
        if movie in user.movies:
            user.movies.remove(movie)
            if len(movie.users) == 0:
                db.session.delete(movie)
            db.session.commit()

    def get_user_movie(self, user_id: int, movie_id: str):
        movie: Movie = db.session.execute(
            db.select(Movie).filter_by(id=movie_id)).scalar_one_or_none()
        user: User = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()

        # data validation
        if not movie:
            raise ValueError(f"Movie with that id: {movie_id} doesnt exist.")
        if not user:
            raise ValueError(f"User with that id: {user_id} doesnt exist.")
        if movie not in user.movies:
            raise ValueError(f"User doesnt have that movie.")

        return self._fetch_movie_data(movie)

    def update_movie_of_user(self, user_id: int, movie_id: str, movie_for_update: dict):
        movie: Movie = db.session.execute(db.select(Movie).filter_by(id=movie_id)).scalar_one_or_none()

        # data validation
        if not movie:
            raise ValueError(f"Movie with id: {movie_id} doesnt exist")
        if movie.name != movie_for_update['name']:
            raise ValueError("You cannot change movie name")
        if not self.is_valid_year(movie_for_update['year']):
            raise ValueError(f"Movie year should be from 1888 to {datetime.now().year}")
        if not self.is_valid_rating(movie_for_update['rating']):
            raise ValueError(
                "Invalid rating. Must be a number (as a string) between 1 and 10 with up to one decimal.")

        movie.director = movie_for_update['director']
        movie.year = movie_for_update['year']
        movie.rating = str(float(movie_for_update['rating']))
        db.session.commit()
    def get_all_public_users(self):
        users = db.session.execute(db.select(User).filter_by(password=None)).scalars()

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
        user: User = db.session.execute(
            db.select(User).filter_by(name=user_name_to_search)).scalar_one_or_none()
        if user and user.password:
            user_to_return = {
                'id': user.id,
                'name': user.name,
                'password': user.password,
                'avatar': user.avatar,
                'movies': [self._fetch_movie_data(movie) for movie in user.movies]
            }
            return user_to_return

    def _fetch_movie_data(self, movie: Movie) -> dict:
        """Creates dict from movie instance and returns it"""
        movie_data_to_return = {"id": movie.id, "name": movie.name, "director": movie.director,
                                "year": movie.year, "rating": movie.rating,
                                "imdb_link": movie.imdb_link, "image_link": movie.image_link
                                }
        return movie_data_to_return

    def is_password_valid(self, user_name: str, password_to_check: str) -> bool:
        """
           Checks the validity of a user's password by comparing a provided
           password with the stored hash of the user's actual password.
        """
        user: User = db.session.execute(
            db.select(User).filter_by(name=user_name)).scalar_one_or_none()

        # checking if stored password of user match the password_to_check
        if user and user.password:
            stored_password_hash = user.password.encode(SQLiteDataManager.ENCODING_TYPE)
            encoded_password_to_check = password_to_check.encode(SQLiteDataManager.ENCODING_TYPE)
            return bcrypt.checkpw(encoded_password_to_check, stored_password_hash)

        return False  # return False for users without a password, or if the user doesn't exist

    def _hash_and_encode_password(self, password: str) -> str:
        """Encodes, hashes, and decodes a given password using bcrypt."""
        password_hash = bcrypt.hashpw(password.encode(SQLiteDataManager.ENCODING_TYPE),
                                      bcrypt.gensalt())
        return password_hash.decode(SQLiteDataManager.ENCODING_TYPE)

    @staticmethod
    def is_valid_rating(rating):
        # Check that rating is a string
        if not isinstance(rating, str):
            return False

        # Attempt to convert the rating to a float
        try:
            float_rating = float(rating)
        except ValueError:
            # Return False if the conversion fails
            return False

        # Check if the float rating is between 1 and 10
        if not (1 <= float_rating <= 10):
            return False

        # Check if the float rating has at most one digit after the decimal
        if '.' in rating and len(rating.split('.')[1]) > 1:
            return False

        return True

    @staticmethod
    def is_valid_year(year):
        # Check if year is a string
        if not isinstance(year, str):
            return False

        # Check for a range of years
        if '–' in year:
            start_year, end_year = year.split('–')

            # Ensure both start and end years are valid individual years
            if not (start_year.isdigit() and end_year.isdigit()):
                return False

            start_year, end_year = int(start_year), int(end_year)

            # Ensure start year is not after end year
            if start_year > end_year:
                return False

            # Check if the end year (for ranges) is between 1888 and the current year
            return 1888 <= end_year <= datetime.now().year

        else:
            # If not a range, check if year is a valid individual year
            if not year.isdigit():
                return False

            # Convert to integer for comparison
            year = int(year)

            # Check if the year is between 1888 and the current year
            return 1888 <= year <= datetime.now().year