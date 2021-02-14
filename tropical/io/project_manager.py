#!/usr/bin/python
import glob, json, os, shutil, sys
from tropical.constants import CONFIG_FILE_NAME, DATA_FILE_NAME, TAGS_DIRECTORY, THEME_DIRECTORY_NAME

class ProjectManager:
    
    def __init__(self, project_directory):
        """Validates that the project directory is valid (exists, has a data-file in it)."""
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
        """Get all content from the project data file, as a JSON object"""
        text_data = ""

        with open("{}/{}".format(self._project_directory, DATA_FILE_NAME), 'r') as file_pointer:
            text_data = file_pointer.read()

        content_data = json.loads(text_data)
        return content_data # JSON type

def recreate_output_directory(output_directory):
    """Recreate the output directory, and any other subdirectories (tags) required for output"""
    if os.path.isdir(output_directory):
        shutil.rmtree(output_directory) # nuke it from orbit

    os.mkdir(output_directory)
    os.mkdir("{}/{}".format(output_directory, TAGS_DIRECTORY))

def copy_required_static_files(project_directory, output_directory):
    """Copy required files (e.g. static/*.js) that are required for Tropical to work (e.g. search)"""
    
    for filename in glob.glob("static/*.js"):
            shutil.copy(filename, output_directory)
    
    shutil.copy("{}/{}".format(project_directory, DATA_FILE_NAME), output_directory)

def copy_theme_files(project_directory, output_directory):
    """Copy any theme files (CSS, JS, PNG, etc.) to the output directory"""
    # copy any directories (images, stylesheets, javascript, etc.) from theme to output
    base_theme_directory = "{}/{}".format(project_directory, THEME_DIRECTORY_NAME)
    for entry in os.scandir(base_theme_directory):
        if os.path.isdir(entry):
            shutil.copytree("{}/{}".format(base_theme_directory, entry.name), "{}/{}".format(output_directory, entry.name))
