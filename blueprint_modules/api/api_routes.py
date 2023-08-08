from flask import Blueprint, request, current_app, jsonify
from data_managers.omdb_api_data_handler import MovieAPIHandler

api_routes = Blueprint('api_routes', __name__)
movies_api_handler = MovieAPIHandler()


@api_routes.route('/api/users', methods=['POST', 'GET'])
def manage_users():
    """
    Endpoint to retrieve all users or add a new user.

    GET:
        Returns a JSON array of all users.

    POST:
        Expects a JSON payload with the following structure:
        {
            'user_name': 'string'  # Required, the name of the user to be added
        }
        Adds a new user and returns a success message.

    :return: JSON response containing users or success/failure message.
    """
    try:
        if request.method == "GET":
            users = current_app.data_manager.get_all_users()
            return jsonify(users), 200

        if request.method == "POST":
            # Check if JSON data is passed
            request_data = request.get_json()
            if request_data is None:
                return jsonify({'error': 'JSON payload is required'}), 400

            # Check if title is present in the JSON data
            user_name_to_add = request_data.get('user_name')
            if user_name_to_add is None:
                return jsonify({'error': 'user name is required'}), 400

            # adding user to db and returning success message
            current_app.data_manager.add_user(user_name_to_add)
            return jsonify({"message": f"User {user_name_to_add} added to library "})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_routes.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    try:
        user_id = int(user_id)
        current_app.data_manager.delete_user(user_id)
        return jsonify({'message': f'User with ID {user_id} successfully deleted.'}), 200


    except TypeError as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@api_routes.route('/api/users/<user_id>/movies')
def get_user_movies(user_id):
    """
    API Endpoint to retrieve movies associated with a specific user.

    Accepts a GET request and takes a user_id as a URL parameter.
    Returns a JSON list of movies associated with the user if found, or an error message if something goes wrong.

    Args:
        user_id(int): The unique identifier of the user for whom to retrieve movies.

    Returns:
        tuple: A JSON response containing the movies associated with the user,
               along with a 200 status code if successful, or an error message and
               corresponding error status code if unsuccessful.
    """
    try:
        movies = current_app.data_manager.get_user_movies(user_id)
        return jsonify(movies), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_routes.route('/api/users/<user_id>/movies', methods=['POST'])
def add_movie_to_user(user_id):
    """
    API Endpoint to add a movie by its title.

    Accepts a POST request with JSON data in the format: {"title": "movie_name"}.
    Returns the added movie in JSON format if successfully added.

    Args:
        request (object): A POST request object containing JSON data with the "title" key.

    Returns:
        dict: A JSON response containing the added movie if successfully added.
    """
    try:
        user_id = int(user_id)

        # Check if JSON data is passed
        request_data = request.get_json()
        if request_data is None:
            return jsonify({'error': 'JSON payload is required'}), 400

        # Check if title is present in the JSON data
        movie_title = request_data.get('title')
        if movie_title is None:
            return jsonify({'error': 'Movie title is required'}), 400

        # search for movie by provided title and validate the data
        movie_data = movies_api_handler.get_movie_by_title(movie_title)
        if movie_data is None:
            return jsonify({'message': f'Movie with name:{movie_title}, not found.'}), 404

        # add movie to db and returns success respond
        current_app.data_manager.add_movie_to_user(user_id, movie_data)
        return jsonify(movie_data), 201

    except TypeError as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_routes.route('/api/users/<user_id>/movies/<movie_id>', methods=['DELETE'])
def delete_movie_of_user(user_id, movie_id):
    """
    Endpoint to delete a movie from a user's collection.

    Takes the user ID and movie ID as parameters, and attempts to delete the specified movie from the specified user's collection.
    Returns a success message with the deleted movie details if successful, or an error message if an exception occurs.

    :param user_id: ID of the user.
    :param movie_id: ID of the movie to delete.
    :return: JSON response indicating success or failure.
    """

    try:
        user_id = int(user_id)
        deleted_movie = current_app.data_manager.delete_movie_of_user(user_id, movie_id)

        return jsonify(
            {'message': f'Movie with ID {movie_id} successfully deleted from user {user_id}.',
             'deleted_movie': deleted_movie}), 200


    except TypeError as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_routes.route('/api/users/<user_id>/movies/<movie_id>/review', methods=['POST','DELETE'])
def review_manager(user_id, movie_id):
    """
    Manages reviews for a given movie and user. Handles both POST (add) and DELETE (remove) requests.

    :param user_id: The ID of the user.
    :param movie_id: The ID of the movie.
    :return: A JSON response with the status of the operation.
    """
    try:
        user_id = int(user_id)

        if request.method == 'DELETE':
            current_app.data_manager.delete_review(user_id, movie_id)
            return jsonify("Successfully deleted review"), 200


        # POST REQUEST HADLING
        # Check if JSON data is passed
        request_data = request.get_json()
        if request_data is None:
            return jsonify({'error': 'JSON payload is required'}), 400

        # Check if title is present in the JSON data
        review = request_data.get('review')
        if review is None:
            return jsonify({'error': 'Movie review is required. No review key in json data'}), 400

        # add review to users movie and return response to user
        current_app.data_manager.update_users_movie_review(user_id,movie_id,review)
        return jsonify({'message': f'Your review added to movie_id {movie_id} of user_id {user_id}'}), 201

    except TypeError as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@api_routes.route('/api/movies/<movie_id>/reviews')
def get_all_review_for_movie(movie_id):
    """
    Retrieves all reviews for a given movie by its ID.

    :param movie_id: The ID of the movie.
    :return: A JSON response containing the reviews or an error message.
    """
    try:
        reviews = current_app.data_manager.get_all_reviews_for_movie(movie_id)
        return jsonify(reviews), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
