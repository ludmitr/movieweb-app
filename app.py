import os
from flask import Flask, request, render_template, redirect, url_for, abort, \
    session
from data_managers.json_data_manager import JSONDataManager
from data_managers.omdb_api_data_handler import MovieAPIHandler
from logging_config.setup_logger import setup_logger

json_data_manager = JSONDataManager('app_data')
movies_api_handler = MovieAPIHandler()
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'KAPUT BARTUXA')

logger = setup_logger()

# ------- ROUTES -------------------------------------------------------------


@app.route('/')
def list_users():
    """Main page endpoint, return rendered page with users"""
    try:
        users = json_data_manager.get_all_public_users()
        session_user = session['username'] if session else None
        return render_template('users.html', users=users,
                               session_user=session_user)
    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@app.route('/user_movies')
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


@app.route('/add_user', methods=["POST"])
def add_user():
    """adding username if passed and returning to the main page"""
    try:
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        if user_name:
            if password:
                json_data_manager.add_user(user_name, password=password)
            else:
                json_data_manager.add_user(user_name)

        return redirect(url_for('list_users'))

    # handling empty string passed or name already exist or password < 6
    except ValueError:
        if password:
            return redirect(url_for('user_register'))

        return redirect(url_for('list_users'))

    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@app.route('/add_movie', methods=['POST'])
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


@app.route("/delete_user/<user_id>", methods=["POST"])
def delete_user(user_id):
    """Deleting user if user id match with passed user_id"""
    try:
        user_id = int(user_id)
        json_data_manager.delete_user(user_id)
        return redirect(url_for('list_users'))
    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@app.route('/users/<int:user_id>/edit_movie/<movie_id>',
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


@app.route('/users/<int:user_id>/delete_movie/<movie_id>', methods=["POST"])
def delete_movie(user_id, movie_id):
    """Delete user's movie if user_id, and movie_id matches"""
    try:
        json_data_manager.delete_movie_of_user(user_id, movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@app.route('/new-user')
def user_register():
    """Render a page to register new user"""
    try:
        return render_template('register_new_user.html')
    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@app.route('/login', methods=['POST'])
def login():
    """
    This Flask route function login handles user login by validating their
    username and password, and on successful validation, stores the user data
    in session and redirects to the 'list_users' route.
    """
    try:
        username = request.form['username']
        password = request.form['password']
        if json_data_manager.is_password_valid(username, password):
            user_data: dict = json_data_manager.get_user_by_name(username)
            session['username'] = user_data
        return redirect(url_for('list_users'))

    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@app.route('/logout')
def logout():
    """
    This Flask route function logout removes user data from the session,
    effectively logging out the user, and then redirects to the 'list_users' route.
    """
    try:
        # remove the username from the session if it's there
        session.pop('username', None)
        return redirect(url_for('list_users'))

    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@app.errorhandler(404)
def page_not_found():
    """Renders a custom '404.html' template whenever a 404 error
    (page not found) occurs in the application
    """
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=5005)
