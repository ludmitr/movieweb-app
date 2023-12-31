from flask import Blueprint, session, request, abort, redirect, url_for, render_template, \
    current_app, flash
from data_managers.omdb_api_data_handler import MovieAPIHandler
from logging_config.setup_logger import setup_logger

movie_routes = Blueprint('movie_routes', __name__)
movies_api_handler = MovieAPIHandler()
logger = setup_logger()


@movie_routes.route('/user_movies')
def user_movies():
    """Render page with movies of specific user"""
    try:
        # render page of user movies if found user by id
        user_id = int(request.args.get('user_id'))
        user_data = current_app.data_manager.get_user_by_id(user_id)
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
                current_app.data_manager.add_movie_to_user(user_id, movie_to_add)

        return redirect(url_for('movie_routes.user_movies', user_id=user_id))
    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@movie_routes.route('/users/<int:user_id>/edit_movie/<movie_id>',
                    methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Update the details of a movie in a user's list. It supports both GET and POST methods.
    -GET: returns rendered page to update/edit movie
    -POST: collects data to update the movie from rendered edit_movie.html and update the movie
    """
    try:
        if request.method == 'GET':
            movie_for_update = current_app.data_manager.get_user_movie(user_id,
                                                                       movie_id)
            return render_template('edit_movie.html', movie=movie_for_update,
                                   user_id=user_id, movie_id=movie_id)

        if request.method == 'POST':
            movie_data_to_update = {}
            for key, value in request.form.items():
                movie_data_to_update[key] = value
            current_app.data_manager.update_movie_of_user(user_id, movie_id,
                                                          movie_data_to_update)
        return redirect(url_for('movie_routes.user_movies', user_id=user_id))
    except ValueError as e:
        flash(str(e))  # adding error message to use it in rendered page
        movie_for_update = current_app.data_manager.get_user_movie(user_id,
                                                                   movie_id)
        return render_template('edit_movie.html', movie=movie_for_update,
                               user_id=user_id, movie_id=movie_id)
    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@movie_routes.route('/users/<int:user_id>/delete_movie/<movie_id>', methods=["POST"])
def delete_movie(user_id, movie_id):
    """Delete user's movie if user_id, and movie_id matches"""
    try:
        current_app.data_manager.delete_movie_of_user(user_id, movie_id)
        return redirect(url_for('movie_routes.user_movies', user_id=user_id))
    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@movie_routes.route('/movies/reviews/add/<int:user_id>/<movie_id>', methods=["GET", "POST"])
def add_review(user_id, movie_id):
    try:
        review = current_app.data_manager.get_users_movie_review(user_id, movie_id)
        if request.method == 'GET':
            return render_template('add_review.html', user_id=user_id, movie_id=movie_id,
                                   review=review)

        if request.method == 'POST':
            # getting data from request and uppdating review
            review_to_update = request.form.get('review')
            current_app.data_manager.update_users_movie_review(user_id, movie_id, review_to_update)

            # creating message to user that will be represented on rendered page
            message_to_user = 'Review updated'
            flash(message_to_user)

            updated_review = current_app.data_manager.get_users_movie_review(user_id, movie_id)
            return render_template('add_review.html', user_id=user_id, movie_id=movie_id,
                                   review=updated_review)

    except ValueError as e:
        flash(str(e))  # adding error message to use it in rendered page
        return render_template('add_review.html', user_id=user_id, movie_id=movie_id, review=review)

    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@movie_routes.route('/movies/<movie_id>/reviews')
def movie_reviews(movie_id):
    # current_app.data_manager.
    movie = current_app.data_manager.get_movie_by_id(movie_id)
    return render_template('movie_reviews.html', movie=movie)


@movie_routes.route('/movies/reviews/delete/<int:user_id>/<movie_id>', methods=['POST'])
def delete_review(user_id: int, movie_id):
    current_app.data_manager.delete_review(user_id, movie_id)
    review = current_app.data_manager.get_users_movie_review(user_id, movie_id)
    flash("Review deleted")
    return render_template('add_review.html', user_id=user_id, movie_id=movie_id, review=review)
