import logging
import os
from flask import Flask, request, render_template, redirect, url_for, abort
from data_managers.json_data_manager import JSONDataManager
from data_managers.omdb_api_data_handler import MovieAPIHandler

json_data_manager = JSONDataManager('movies_test_2')
movies_api_handler = MovieAPIHandler()

# set up log file path for logs
log_dir = 'logs'
log_file = 'app.log'
log_path = os.path.join(log_dir, log_file)

# Create or get the logger
logger = logging.getLogger(__name__)  # __name__ resolves to the name of the module, class, or function that called this logging setup

# set log level
logger.setLevel(logging.ERROR)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

handler = logging.FileHandler(log_path)  # set the log handler
handler.setLevel(logging.ERROR)  # set the handler level

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # create a logging format
handler.setFormatter(formatter)  # set the logging format for the handler

logger.addHandler(handler)

app = Flask(__name__)


# ------- ROUTES -------------------------------------------------------------

@app.route('/')
def list_users():
    """Main page endpoint, return rendered page with users"""
    try:
        users = json_data_manager.get_all_users()
        return render_template('users.html', users=users)
    except Exception as e:
        abort(404)

@app.route('/user_movies')
def user_movies():
    try:
        # render page of user movies if found user by id
        user_id = int(request.args.get('user_id'))
        user = json_data_manager.get_user_by_id(user_id)
        if user:
            return render_template('user_movies.html', user=user)

        # if user id not found redirect to main page
        return redirect(url_for("list_users"))

    except Exception as e:
        logger.exception("Exception occurred")
        abort(404)


@app.route('/add_user', methods=["POST"])
def add_user():
    """adding username if passed and returning to the main page"""
    try:
        user_name = request.form.get('user_name')
        if user_name:
            json_data_manager.add_user(user_name)

        return redirect(url_for('list_users'))
    except Exception as e:
        logger.exception("Exception occurred")
        abort(404)

@app.route('/add_movie', methods=['POST'])
def add_movie():
    try:
        movie_name_to_search: str = request.form.get('search_name')
        user_id = int(request.form.get('user_id'))
        if movie_name_to_search:
            movie_to_add = movies_api_handler.get_movie_by_title(
                movie_name_to_search)
            if movie_to_add:
                json_data_manager.add_movie_to_user(user_id, movie_to_add)

        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        logger.exception("Exception occurred")
        abort(404)


@app.route("/delete_user/<user_id>", methods=["POST"])
def delete_user(user_id):
    try:
        user_id = int(user_id)
        json_data_manager.delete_user(user_id)
        return redirect(url_for('list_users'))
    except Exception as e:
        logger.exception("Exception occurred")
        abort(404)

@app.route('/users/<int:user_id>/edit_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    try:
        if request.method == 'GET':
            movie_for_update = json_data_manager.get_user_movie(user_id, movie_id)
            return render_template('edit_movie.html', movie=movie_for_update,
                                   user_id=user_id, movie_id=movie_id)

        if request.method == 'POST':
            movie_data_to_update = {}
            for key, value in request.form.items():
                movie_data_to_update[key] = value
            json_data_manager.update_movie_of_user(user_id, movie_id,
                                                   movie_data_to_update)

        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        logger.exception("Exception occurred")
        abort(404)


@app.route('/users/<int:user_id>/delete_movie/<movie_id>', methods=["POST"])
def delete_movie(user_id, movie_id):
    try:
        json_data_manager.delete_movie_of_user(user_id, movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        logger.exception("Exception occurred")
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)

