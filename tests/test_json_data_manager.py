from data_managers.json_data_manager import JSONDataManager
import os
import pytest

FILE_NAME = "test_data_manager"
DATA_FOLDER_NAME = 'data'


def test_create_new_manager():
    # creating new instance for JSONDataManager. checking if file created and deleting the file
    json_manager = JSONDataManager(FILE_NAME)
    file_path = os.path.join(DATA_FOLDER_NAME, FILE_NAME + '.json')
    assert os.path.exists(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)

def test_add_user():
    json_manager = JSONDataManager(FILE_NAME)
    file_path = os.path.join(json_manager.file_name)

    # test adding new user
    json_manager.add_user("bob")
    users = json_manager.get_all_users()
    assert users[0]['name'] == 'bob'
    assert users[0]['id'] == 1

    # test passing not string variable will raise an error
    with pytest.raises(TypeError):
        json_manager.add_user(2)

    # passing empty string raise an error
    with pytest.raises(ValueError):
        json_manager.add_user('')

    # passing name that already exists
    with pytest.raises(ValueError):
        json_manager.add_user('bob')


    if os.path.exists(file_path):
        os.remove(file_path)


pytest.main()