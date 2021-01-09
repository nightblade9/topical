from tropical.constants import CONFIG_FILE_NAME
import json, os

def get_config(project_directory):
    """
        Gets the project configuration from the target directory, if it exists.
        If it doesn't exist, returns an empty dictionary ({}).
    """
    config_json_path = "{}/{}".format(project_directory, CONFIG_FILE_NAME)
    config_json = {}
    if os.path.isfile(config_json_path):
        with open(config_json_path) as file_handle:
            raw_json = file_handle.read()
            config_json = json.loads(raw_json)
    
    return config_json
    