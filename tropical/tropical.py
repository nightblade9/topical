#!/usr/bin/python

import sys

class Tropical:
    def __init__(self):
        pass

    def run(self, args):
        print("Hello, Tropical! {}".format(args))
        
        if len(args) != 2:
            print("Usage: python main.py <tropical project directory>")
            sys.exit(1)

        project_directory = args[1]
        if len(project_directory.strip()) == 0:
            print("Please specify a non-empty project directory")
            sys.exit(2)
        
