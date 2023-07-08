import os
from flask import Flask, render_template, abort, session
from logging_config.setup_logger import setup_logger
from blueprint_modules.user.user_routes import user_routes
from blueprint_modules.movie.movie_routes import movie_routes
from config import json_data_manager

app = Flask(__name__)
app.register_blueprint(user_routes)
app.register_blueprint(movie_routes)
app.secret_key = os.environ.get('SECRET_KEY', 'KAPUT BARTUXA')
logger = setup_logger()

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


@app.errorhandler(404)
def page_not_found(e):
    """Renders a custom '404.html' template whenever a 404 error
    (page not found) occurs in the application
    """
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=5005)
