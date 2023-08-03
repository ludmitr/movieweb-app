from flask import Blueprint, session, request, abort, redirect, url_for, \
    render_template, flash, current_app
from data_managers.omdb_api_data_handler import MovieAPIHandler
from logging_config.setup_logger import setup_logger
from config import json_data_manager
from data_managers import sql_data_manager

user_routes = Blueprint('user_routes', __name__)
movies_api_handler = MovieAPIHandler()
logger = setup_logger()


@user_routes.route('/users', methods=["POST"])
def add_user():
    """adding username if passed and returning to the main page"""
    try:
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        if user_name:
            if password:
                current_app.sql_data_manager.add_user(user_name, password=password)
            else:
                current_app.sql_data_manager.add_user(user_name)

        return redirect(url_for('list_users'))

    # handling empty string passed or name already exist or password < 6
    except ValueError as e:
        flash(str(e))  # adding error message to use it in rendered page
        if password:
            return redirect(url_for('user_routes.user_register'))

        return redirect(url_for('list_users'))

    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@user_routes.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deleting user if user id match with passed user_id"""
    try:
        user_id = int(user_id)
        json_data_manager.delete_user(user_id)
        return redirect(url_for('list_users'))
    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@user_routes.route('/new-user')
def user_register():
    """Render a page to register new user"""
    try:
        return render_template('register_new_user.html')
    except Exception:
        logger.exception("Exception occurred")
        abort(404)


@user_routes.route('/login', methods=['POST'])
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


@user_routes.route('/logout')
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
