#!/usr/bin/python
import os, sys

class ProjectValidator:
    
    def __init__(self, project_directory):
        if len(project_directory.strip()) == 0:
            print("Please specify a non-empty project directory")
            sys.exit(2)

        if not os.path.isdir(project_directory):
            print("Project directory {} doesn't exist or isn't a directory".format(project_directory))
            sys.exit(3)

        self._project_directory = project_directory

    def get_config(self):
        return {}