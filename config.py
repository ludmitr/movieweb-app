from data_managers.json_data_manager import JSONDataManager

# making sure using same data handler file across modules for endpoint routes
json_data_manager = JSONDataManager('app_data')
