from flask import Blueprint, session, request, abort, redirect, url_for, render_template
from data_managers.omdb_api_data_handler import MovieAPIHandler
from logging_config.setup_logger import setup_logger
from config import json_data_manager

movie_routes = Blueprint('movie_routes', __name__)
movies_api_handler = MovieAPIHandler()
logger = setup_logger()

@movie_routes.route('/user_movies')
def user_movies():
    """Render page with movies of specific user"""
    try:
        # render page of user movies if found user by id
        user_id = int(request.args.get('user_id'))
        user_data = json_data_manager.get_user_by_id(user_id)
        session_user = session['username'] if session else None
        if user_data:
            return render_template('user_movies.html', user=user_data,
                                   session_user=session_user)

        # if user id not found redirect to main page
        return redirect(url_for("list_users"))

    except Exception:
        logger.exception("Exception occurred")
        abort(404)

@movie_routes.route('/add_movie', methods=['POST'])
def add_movie():
    """Adding movie to user movies list. The movie information is fetched from
    an external movies API (OMDb) based on the search name passed in the POST request."""
    try:
        # adding movie from omdb - if found
        movie_name_to_search: str = request.form.get('search_name')
        user_id = int(request.form.get('user_id'))
        if movie_name_to_search:
            movie_to_add = movies_api_handler.get_movie_by_title(
                movie_name_to_search)
            if movie_to_add:
                json_data_manager.add_movie_to_user(user_id, movie_to_add)

        return redirect(url_for('user_movies', user_id=user_id))
    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@movie_routes.route('/users/<int:user_id>/edit_movie/<movie_id>',
           methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Update the details of a movie in a user's list.
    It supports both GET and POST methods.
    GET: returns rendered page to update/edit movie
    POST: collects data to update the movie from rendered edit_movie.html and
    update the movie
    """
    try:
        if request.method == 'GET':
            movie_for_update = json_data_manager.get_user_movie(user_id,
                                                                movie_id)
            return render_template('edit_movie.html', movie=movie_for_update,
                                   user_id=user_id, movie_id=movie_id)

        if request.method == 'POST':
            movie_data_to_update = {}
            for key, value in request.form.items():
                movie_data_to_update[key] = value
            json_data_manager.update_movie_of_user(user_id, movie_id,
                                                   movie_data_to_update)

        return redirect(url_for('user_movies', user_id=user_id))
    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@movie_routes.route('/users/<int:user_id>/delete_movie/<movie_id>', methods=["POST"])
def delete_movie(user_id, movie_id):
    """Delete user's movie if user_id, and movie_id matches"""
    try:
        json_data_manager.delete_movie_of_user(user_id, movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception:
        logger.exception("Exception occurred")
        abort(404)
