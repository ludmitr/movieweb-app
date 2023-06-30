from flask import Flask, request, render_template, redirect, url_for
from data_managers.json_data_manager import JSONDataManager
from data_managers.omdb_api_data_handler import MovieAPIHandler

import logging
import os


# if not os.path.exists('logs'):
#     os.makedirs('logs')
#
# logging.basicConfig(filename='logs/app.log', level=logging.INFO)

app = Flask(__name__)


#------- ROUTES -------------------------------------------------------------


@app.route('/')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/user_movies', methods=["POST"])
def user_movies():
    user_id = int(request.form.get('user_id'))
    user_name = request.form.get('user_name')
    movies = data_manager.get_user_movies(user_id)

    return render_template('user_movies.html', user_movies=movies, user_name=user_name, user_id=user_id)


@app.route('/add_user')
def add_user():
    user_name = request.args.get('user_name')
    if user_name:
        data_manager.add_user(user_name)

    return redirect(url_for('list_users'))
    #  This route will present a form that enables the addition of a new user to our MovieWeb App.


@app.route('/add_movie', methods=['POST'])
def add_movie():
    movie_name_to_search: str = request.form.get('search_name')
    user_id = int(request.form.get('user_id'))
    if movie_name_to_search:
        movie_to_add = movies_api_handler.get_movie_by_title(movie_name_to_search)
        if movie_to_add:
            data_manager.add_movie_to_user(user_id, movie_to_add)
    user = data_manager.get_user_by_id(user_id)
    return render_template('user_movies.html', user_movies=user['movies'], user_name=user['name'], user_id=user['id'])







@app.route("/delete_user/<int:user_id>")
def delete_user(user_id: int):
    data_manager.delete_user(user_id)

    return redirect(url_for('list_users'))


@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie(user_id, movie_id):
    pass
    #This route will display a form allowing for the updating of details of a
    # specific movie in a user’s list.


@app.route('/users/<user_id>/edit_movie/<movie_id>')
def edit_movie(user_id, movie_id):
    pass
    # This route will show a form allowing the modification of a specific
    # movie in a user’s favorite movie list.


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    pass
    # : Upon visiting this route, a specific movie will be removed from a
    # user’s favorite movie list.


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    data_manager = JSONDataManager('movies_test_2')
    movies_api_handler = MovieAPIHandler()
    app.run(port=5000, debug=True)

