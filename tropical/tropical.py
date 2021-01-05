#!/usr/bin/python

import os, shutil, sys, time
from tropical.constants import OUTPUT_DIRECTORY, TAGS_DIRECTORY
from tropical.io.project_validator import ProjectValidator
from tropical.io.themer import Themer

class Tropical:
    def __init__(self):
        pass

    def run(self, args):
        if len(args) != 2:
            print("Usage: python main.py <tropical project directory>")
            sys.exit(1)

        project_directory = args[1]

        content_data = ProjectValidator(project_directory).get_data()
        themer = Themer(project_directory) # validate theme directory

        start_time = time.time()
        
        all_files = themer.generate_output(content_data)
        output_directory = "{}/{}".format(project_directory, OUTPUT_DIRECTORY)

        if os.path.isdir(output_directory):
            shutil.rmtree(output_directory) # nuke it from orbit

        os.mkdir(output_directory)
        os.mkdir("{}/{}".format(output_directory, TAGS_DIRECTORY))

        num_tags = 0

        for filename in all_files:
            contents = all_files[filename]
            output_filename = "{}/{}".format(output_directory, filename)

            if TAGS_DIRECTORY in filename:
                num_tags += 1

            with open(output_filename, 'w') as file_pointer:
                file_pointer.write(contents)
                file_pointer.close()

        stop_time = time.time()
        
        site_summary = "{} pages and {} items across {} tags".format(len(all_files), len(content_data), num_tags)
        print("{} - generated in {}s".format(site_summary, (stop_time - start_time)))