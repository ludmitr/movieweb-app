import os
from flask import Flask, render_template, abort, session, current_app, flash, redirect, url_for
import config
from logging_config.setup_logger import setup_logger
from blueprint_modules.user.user_routes import user_routes
from blueprint_modules.movie.movie_routes import movie_routes
from blueprint_modules.api.api_routes import api_routes
from data_managers.omdb_api_data_handler import MovieAPIHandler
from data_managers.sql_data_manager import SQLiteDataManager

# Initialize the Flask application
app = Flask(__name__)

# Register blueprints for user, movie, and API routes
app.register_blueprint(user_routes)
app.register_blueprint(movie_routes)
app.register_blueprint(api_routes)

# Set the secret key for session management, with a fallback value
app.secret_key = os.environ.get('SECRET_KEY', 'KAPUT BARTUXA')

app.data_manager = SQLiteDataManager(config.SQL_DB_FILE_NAME, app)
logger = setup_logger()

@app.route('/')
def list_users():
    """Main page endpoint, return rendered page with users"""
    try:
        users = current_app.data_manager.get_all_public_users()
        session_user = session['username'] if 'username' in session else None
        return render_template('users.html', users=users,
                               session_user=session_user)
    except Exception:
        logger.exception("Exception occurred")
        abort(404)

@app.route('/api_faq')
def api_explain():
    return render_template('api_explain.html')

@app.route('/restore_data')
def restore_default_db():
    app.data_manager.restore_db_to_default()
    message_for_user = 'Database RESTORED!'
    flash(message_for_user)
    return redirect(url_for('list_users'))

@app.errorhandler(404)
def page_not_found(e):
    """Renders a custom '404.html' template whenever a 404 error
    (page not found) occurs in the application
    """
    return render_template('404.html'), 404


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(port=5005, debug=True)
