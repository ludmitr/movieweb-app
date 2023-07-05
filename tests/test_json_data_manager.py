from data_managers.json_data_manager import JSONDataManager
import os
import pytest

FILE_NAME = "test_data_manager"
DATA_FOLDER_NAME = 'data'
FILE_PATH = os.path.join(DATA_FOLDER_NAME, FILE_NAME + '.json')

@pytest.fixture
def json_manager():
    manager = JSONDataManager(FILE_NAME)
    yield manager
    # Teardown
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)

def test_file_created_after_manager_initialization(json_manager):
    assert os.path.exists(FILE_PATH)

def test_add_valid_user(json_manager):
    json_manager.add_user("bob")
    users = json_manager.get_all_users()
    assert users[0]['name'] == 'bob'
    assert users[0]['id'] == 1

def test_add_user_with_integer_name(json_manager):
    with pytest.raises(TypeError):
        json_manager.add_user(2)

def test_add_user_with_empty_string(json_manager):
    with pytest.raises(ValueError):
        json_manager.add_user('')

def test_add_user_with_existing_name(json_manager):
    json_manager.add_user("bob")
    with pytest.raises(ValueError):
        json_manager.add_user('bob')

def test_movie_added_to_user(json_manager):
    json_manager.add_user("bob")
    movie_to_add = {"id": "tt0091757", "name": "Pirates",
                    "director": "Roman Polanski",
                    "year": "1986", "rating": "6.0",
                    "imdb_link": "https://www.test.com",
                    "image_link": "https:test-link.jpg"
                    }
    json_manager.add_movie_to_user(1, movie_to_add)
    added_movie = json_manager.get_user_movie(1, movie_to_add['id'])
    assert added_movie == movie_to_add

def test_delete_movie_of_user(json_manager):
    json_manager.add_user("bob")
    movie_to_add = {"id": "tt0091757", "name": "Pirates",
                    "director": "Roman Polanski",
                    "year": "1986", "rating": "6.0",
                    "imdb_link": "https://www.test.com",
                    "image_link": "https:test-link.jpg"
                    }
    # adding movie to user
    json_manager.add_movie_to_user(1, movie_to_add)

    # deleting movie from user and testing that it deleted
    json_manager.delete_movie_of_user(1, movie_to_add['id'])
    users = json_manager.get_all_users()
    assert len(users[0]['movies']) == 0, "movie deleted"


def test_delete_movie_of_unexisted_user(json_manager):
    error_message = 'User with id 1 does not exist'
    with pytest.raises(ValueError, match=error_message):
        json_manager.delete_movie_of_user(1, 'fdfd33refd')

def test_delete_movie_that_does_not_exist(json_manager):
    error_message = 'User with id 1 does not exist'
    with pytest.raises(ValueError, match=error_message):
        json_manager.delete_movie_of_user(1, 'fdfd33refd')

pytest.main()
