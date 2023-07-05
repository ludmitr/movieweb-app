# python -m pytest .\tests\test_flask_app.py::test_add_user  to run specific function test from terminal
import pytest
from unittest.mock import MagicMock, patch
from flask import url_for
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    ctx = app.test_request_context()  # Create a test request context
    ctx.push()  # Push the context

    with app.test_client() as client:
        yield client

    ctx.pop()  # Don't forget to pop the context to clean up at the end


@patch('app.json_data_manager.get_all_users')
def test_main_page(mock_get_all_users, client):
    mock_get_all_users.return_value = [{"id": 1, "name": "Alice", "movies": []},
                                       {"id": 2, "name": "Diksi", "movies": []}]
    response = client.get(url_for("list_users"))

    assert response.status_code == 200
    assert b'Alice' in response.data
    assert b'Diksi' in response.data


@patch('app.json_data_manager.get_user_by_id')
def test_user_movies(mock_get_user_by_id, client):
    end_point_func_name = 'user_movies'

    # mocking response of user, and rendering page with user data
    mock_get_user_by_id.return_value = {"id": 3, "name": "TEST_NAME", "movies": []}
    response = client.get(url_for(end_point_func_name, user_id=3))
    assert response.status_code == 200
    assert b'TEST_NAME' in response.data  # checking if name is in rendered html page

    # case when app.data_manager.get_user_by_id raise TypeErrpr
    mock_get_user_by_id.side_effect = TypeError("Error: Invalid user ID")
    response = client.get(url_for(end_point_func_name, user_id="3"))
    assert response.status_code == 404
    mock_get_user_by_id.side_effect = None

    # case when app.data_manager.get_user_by_id returns None
    mock_get_user_by_id.return_value = None
    response = client.get(url_for("user_movies", user_id=-1))
    assert response.status_code == 302, "redirect to 404 page"


@patch('app.json_data_manager.add_user')
def test_add_user(mock_dm_add_user, client):
    # case when adding legit name
    response = client.post(url_for('add_user'), data={'user_name': 'shmiksi'})
    assert response.status_code == 302, "redirect to main page"

    # case of adding empty name
    response = client.post(url_for('add_user'), data={'user_name': ''})
    assert response.status_code == 302, "if user name emppty it doesnt add to db"


@patch('app.json_data_manager.add_movie_to_user')
@patch('app.movies_api_handler.get_movie_by_title')
def test_add_movie(mock_get_movie_by_title, mock_add_movie_to_user, client):
    mock_get_movie_by_title.return_value = {
        "id": "tt0120338",
        "name": "Titanic",
        "director": "James Cameron",
        "year": "1997",
        "rating": "7.9",
        "imdb_link": "https://www.imdb.com/title/tt0120338",
        "image_link": "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg"
    }

    # case of passing wrong id, should raise an error and return 404 page
    response = client.post(url_for('add_movie'), data={'search_name': 'titanic', 'id': 'b'})
    assert response.status_code == 404

    # passing right data and checking if all worked as supposed to
    response = client.post(url_for('add_movie'), data={'search_name': 'titanic', 'user_id': '1'})
    response.status_code = 302  # redirecting to page with all user movies
    assert response.location == url_for('user_movies', user_id=1)  # checking redirect url
    mock_get_movie_by_title.assert_called_once_with('titanic')
    mock_add_movie_to_user.assert_called_once()

    response = client.post(url_for('add_movie'),
                           data={'search_name': 'titanic', 'user_id': '-1'})


@patch('app.json_data_manager.delete_user')
def test_delete_user(mock_delete_user, client):
    # id found and deleted or not found  - redirect to the main page
    response = client.post(url_for('delete_user', user_id=1))
    mock_delete_user.assert_called_once_with(1)
    assert response.status_code == 302
    assert response.location == url_for('list_users')

    # case when passed user id is not convertible to integer
    response = client.post(url_for('delete_user', user_id='b'))
    assert response.status_code == 404
@patch('app.json_data_manager.get_user_movie')
@patch('app.json_data_manager.update_movie_of_user')
def test_update_movie(mock_movie_update, mock_get_user_movie, client):
    # case of passing valid POST update data
    movie_data_for_update = {"director": "Nikita Mikhalkov", "year": "2007", "rating": "7.6"}
    response = client.post(url_for('update_movie', user_id=1, movie_id='sd34f44'), data=movie_data_for_update)
    mock_movie_update.assert_called_once()
    assert response.status_code == 302
    assert response.location == url_for('user_movies', user_id=1)

    # GET method - test valid data case
    mock_get_user_movie.return_value ={"id": "tt0488478",
                                       "name": "12",
                                       "director": "Nikita Mikhalkov",
                                       "year": "2007", "rating": "7.6",
                                       "imdb_link": "https://www.imdb.com/title/tt0488478",
                                       "image_link": "https://m.media-amazon.com/images/M/MV5BNDExOTBkMWYtYWE1MS00OGYzLTg4OWMtNDgxMjZjZDM3NGM3XkEyXkFqcGdeQXVyMTA0MTM5NjI2._V1_SX300.jpg"
                                       }
    response = client.get(url_for('update_movie', user_id=1, movie_id='sd34f44'))
    assert response.status_code == 200
    mock_get_user_movie.assert_called_once()
    assert b'2007' in response.data
    assert b'Nikita Mikhalkov' in response.data

    # case of not passing movie id
    response = client.get('/users/5/edit_movie/')
    assert response.status_code == 404



pytest.main()