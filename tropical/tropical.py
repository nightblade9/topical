#!/usr/bin/python

import sys
from tropical.io.project_validator import ProjectValidator
from tropical.io.themer import Themer

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
        Themer(project_directory) # validate theme directory