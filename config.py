from data_managers.json_data_manager import JSONDataManager
from data_managers.sql_data_manager import SQLiteDataManager
import os
DB_DEFAULT_NAME = 'movies.sqlite'


# making sure using same data handler file across modules for endpoint routes
json_data_manager = JSONDataManager('app_data')

def get_absolute_db_uri(db_name):
    current_folder = os.path.abspath(os.getcwd())
    db_path = os.path.join(current_folder, 'data', db_name)
    return 'sqlite:///' + db_path
