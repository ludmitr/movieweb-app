from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# association table for the many-to-many relationship between User and Movie
user_movie_association = db.Table('user_movie',
                                  db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                                  db.Column('movie_id', db.String, db.ForeignKey('movies.id')))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    avatar = db.Column(db.String)
    movies = db.relationship(
        "Movie",
        secondary=user_movie_association,
        back_populates="users",
    )


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    director = db.Column(db.String)
    year = db.Column(db.String)
    rating = db.Column(db.String)
    imdb_link = db.Column(db.String)
    image_link = db.Column(db.String)
    users = db.relationship(
        "User",
        secondary=user_movie_association,
        back_populates="movies"
    )


