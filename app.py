from flask import Flask, request, render_template, redirect, url_for
from data_managers.json_data_manager import JSONDataManager
app = Flask(__name__)
data_manager = JSONDataManager('movies_test_2')

#------- ROUTES -------------------------------------------------------------


# @app.route('/')
# def home():
#     return "Welcome to MovieWeb App!"
#     #This will be the home page of our application. You have the creative
#     # liberty to design this as a simple welcome screen or a more elaborate dashboard.


@app.route('/')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/user_movies', methods=["POST"])
def user_movies():
    user_id = int(request.form.get('user_id'))
    user_name = request.form.get('user_name')
    movies = data_manager.get_user_movies(user_id)

    return render_template('user_movies.html', user_movies=movies, user_name=user_name)


@app.route('/add_user')
def add_user():
    user_name = request.args.get('user_name')
    if user_name:
        data_manager.add_user(user_name)

    return redirect(url_for('list_users'))
    #  This route will present a form that enables the addition of a new user to our MovieWeb App.


@app.route('/users/<user_id>')
def add_movie(user_id):
    pass
    # This route will display a form to add a new movie to a user’s list of favorite movies.

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
    app.run(port=5000, debug=True)

