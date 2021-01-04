#!/usr/bin/python
import json, os, sys
from tropical.constants import DATA_FILE_NAME

class ProjectValidator:
    
    def __init__(self, project_directory):
        if len(project_directory.strip()) == 0:
            print("Please specify a non-empty project directory")
            sys.exit(2)

        if not os.path.isdir(project_directory):
            print("Project directory {} doesn't exist or isn't a directory".format(project_directory))
            sys.exit(3)

        if not os.path.isfile("{}/{}".format(project_directory, DATA_FILE_NAME)):
            print("Can't find config file {}\{}".format(project_directory, DATA_FILE_NAME))
            sys.exit(4)

        self._project_directory = project_directory

    def get_data(self):
        text_data = ""

        with open("{}/{}".format(self._project_directory, DATA_FILE_NAME), 'r') as file_pointer:
            text_data = file_pointer.read()

        content_data = json.loads(text_data)
        return content_data
