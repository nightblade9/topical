#!/usr/bin/python

import glob, json, os, shutil, sys, time
from tropical.constants import OUTPUT_DIRECTORY, TAGS_DIRECTORY, THEME_DIRECTORY_NAME, CONFIG_FILE_NAME
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

        start_time = time.time()

        content_data = ProjectValidator(project_directory).get_data()
        themer = Themer(project_directory) # validate theme directory
        
        config_file_path = "{}/{}".format(project_directory, CONFIG_FILE_NAME)
        config_file = {}
        if os.path.isfile(config_file_path):
            with open(config_file_path) as file_handle:
                config_file = json.loads(file_handle.read())

        output = themer.generate_output(content_data, config_file)
        all_files = output["data"]
        stats = output["stats"]
        output_directory = "{}/{}".format(project_directory, OUTPUT_DIRECTORY)

        if os.path.isdir(output_directory):
            shutil.rmtree(output_directory) # nuke it from orbit

        os.mkdir(output_directory)
        os.mkdir("{}/{}".format(output_directory, TAGS_DIRECTORY))

        for filename in all_files:
            contents = all_files[filename]
            output_filename = "{}/{}".format(output_directory, filename)

            with open(output_filename, 'w') as file_pointer:
                file_pointer.write(contents)
                file_pointer.close()

        # copy static JS required for tropical functions (search)
        for filename in glob.glob("static/*.js"):
            shutil.copy(filename, output_directory)
        
        # copy any directories (images, stylesheets, javascript, etc.) from theme to output
        base_theme_directory = "{}/{}".format(project_directory, THEME_DIRECTORY_NAME)
        for entry in os.scandir(base_theme_directory):
            if os.path.isdir(entry):
                shutil.copytree("{}/{}".format(base_theme_directory, entry.name), "{}/{}".format(output_directory, entry.name))

        stop_time = time.time()
        
        print("{}, totaling {} pages - generated in {}s".format(stats, len(all_files), (stop_time - start_time)))