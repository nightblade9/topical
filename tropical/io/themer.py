#!/usr/bin/python
import os, sys

from tropical.html import search_html_generator
from tropical.constants import THEME_DIRECTORY_NAME, LAYOUT_FILE_NAME, SNIPPET_FILE_NAME

class Themer:
    def __init__(self, project_directory):
        if len(project_directory.strip()) == 0:
            print("Please specify a non-empty project directory")
            sys.exit(2)

        if not os.path.isdir(project_directory):
            print("Project directory {} doesn't exist or isn't a directory".format(project_directory))
            sys.exit(3)

        theme_directory = "{}/{}".format(project_directory, THEME_DIRECTORY_NAME)
        if not os.path.isdir(theme_directory):
            print("Theme directory ({}) missing from project directory".format(theme_directory))
            sys.exit(4)
        
        if not _check_theme_files(theme_directory):
            sys.exit(5)

        self._project_directory = project_directory
        self._theme_directory = theme_directory

        # load/cache layout HTML
        with open("{}/{}/{}".format(self._project_directory, THEME_DIRECTORY_NAME, LAYOUT_FILE_NAME), 'r') as file_pointer:
            self._layout_html = file_pointer.read()

    def apply_layout_html(self, content_html, title, config_json, add_search_form = True):
        """
        Applies the theme layout to the target HTML.
        Swaps in the specified title.
        Adds a search form to the body, if add_search_form is True.
        Also substitutes in {siteRootUrl} if specified.
        """

        root_url = ""
        if "siteRootUrl" in config_json:
            root_url = config_json["siteRootUrl"]

        final_html = self._layout_html.replace("{content}", content_html) \
            .replace("{pageTitle}", title) \
            .replace("{siteRootUrl}", root_url)

        search_html = ""
        if add_search_form:
            search_html = search_html_generator.get_search_html()
        final_html = final_html.replace("{search}", search_html)

        return final_html

def _check_theme_files(theme_directory):
    if not os.path.isfile("{}/{}".format(theme_directory, LAYOUT_FILE_NAME)):
        print("Theme is missing layout file {}".format(LAYOUT_FILE_NAME))
        return False
    
    if not os.path.isfile("{}/{}".format(theme_directory, SNIPPET_FILE_NAME)):
        print("Theme is missing snippet file {}".format(SNIPPET_FILE_NAME))
        return False
    
    return True