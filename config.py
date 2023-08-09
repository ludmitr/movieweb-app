from data_managers.json_data_manager import JSONDataManager
from data_managers.sql_data_manager import SQLiteDataManager
import os

SQL_DB_FILE_NAME = 'movies.sqlite'
SQL_DB_DEFAULT_NAME = 'default_movies.sqlite'
JSON_DB_DEFAULT_NAME = "app_data"  # you can change and new file will be created -> new_file.json

def get_absolute_db_uri(db_name):
    current_folder = os.path.abspath(os.getcwd())
    db_path = os.path.join(current_folder, 'data', db_name)
    return 'sqlite:///' + db_path

def get_json_data_manager():
    return JSONDataManager(JSON_DB_DEFAULT_NAME)

def get_absolute_path_to_project_folder_folders(folder_name: str):
    project_folder_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(project_folder_path, folder_name)


def get_absolute_path_current_db():
    abs_path_data = get_absolute_path_to_project_folder_folders('data')
    return os.path.join(abs_path_data, SQL_DB_FILE_NAME)


def get_absolute_path_default_db():
    abs_path_data = get_absolute_path_to_project_folder_folders('data')
    return os.path.join(abs_path_data, SQL_DB_DEFAULT_NAME)