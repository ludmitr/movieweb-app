from data_managers.json_data_manager import JSONDataManager
from data_managers.sql_data_manager import SQLiteDataManager
import os

DB_DEFAULT_NAME = 'movies.sqlite'  # without option to change
JSON_DB_DEFAULT_NAME = "app_data"  # you can change and new file will be created -> new_file.json

def get_absolute_db_uri(db_name):
    current_folder = os.path.abspath(os.getcwd())
    db_path = os.path.join(current_folder, 'data', db_name)
    return 'sqlite:///' + db_path

def get_json_data_manager():
    return JSONDataManager(JSON_DB_DEFAULT_NAME)

def get_sqlite_data_manager(app):
    return SQLiteDataManager(DB_DEFAULT_NAME, app)
