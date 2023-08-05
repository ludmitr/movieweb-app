import os
from flask import Flask, render_template, abort, session, current_app
from data_managers.data_models_for_sql import db
import config
from logging_config.setup_logger import setup_logger
from blueprint_modules.user.user_routes import user_routes
from blueprint_modules.movie.movie_routes import movie_routes
from data_managers.sql_data_manager import SQLiteDataManager

app = Flask(__name__)
app.register_blueprint(user_routes)
app.register_blueprint(movie_routes)
app.secret_key = os.environ.get('SECRET_KEY', 'KAPUT BARTUXA')
app.sql_data_manager = SQLiteDataManager(config.DB_DEFAULT_NAME, app)
db.init_app(app)
logger = setup_logger()

@app.route('/')
def list_users():
    """Main page endpoint, return rendered page with users"""
    try:
        users = current_app.sql_data_manager.get_all_public_users()
        session_user = session['username'] if 'username' in session else None
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
    # with app.app_context():
    #     db.create_all()
    app.run(port=5005, debug=True)
