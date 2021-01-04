#!/usr/bin/python

import sys
from tropical.io.project_validator import ProjectValidator

class Tropical:
    def __init__(self):
        pass

    def run(self, args):
        print("Hello, Tropical! {}".format(args))
        
        if len(args) != 2:
            print("Usage: python main.py <tropical project directory>")
            sys.exit(1)

        project_directory = args[1]

        content_data = ProjectValidator(project_directory).get_data()
        print("Gotcha, data is: {}".format(content_data))

        