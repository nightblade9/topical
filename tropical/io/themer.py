#!/usr/bin/python
import json, os, sys
from tropical.constants import THEME_DIRECTORY_NAME, LAYOUT_FILE_NAME, SNIPPET_FILE_NAME, INDEX_FILENAME

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

        with open("{}/{}/{}".format(self._project_directory, THEME_DIRECTORY_NAME, LAYOUT_FILE_NAME), 'r') as file_pointer:
            self._layout_html = file_pointer.read()

    def generate_output(self, content_data):
        blurbs = self._get_snippets_html(content_data)

        all_files = {} # filename => content

        all_files[INDEX_FILENAME] = self._apply_layout_html(str.join("\n", blurbs), "Home")
        return all_files
    
    def _apply_layout_html(self, content_html, title):
        final_html = self._layout_html.replace("{content}", content_html)
        # TODO: site name comes from config
        final_html = final_html.replace("{pageTitle}", title).replace("{siteName}", "Game Design Library")
        return final_html

    def _get_snippets_html(self, content_json):
        snippets_template = ""

        with open("{}/{}/{}".format(self._project_directory, THEME_DIRECTORY_NAME, SNIPPET_FILE_NAME), 'r') as file_pointer:
            snippets_template = file_pointer.read()

        html_snippets = []

        for item in content_json:
            item_html = snippets_template.replace("{title}", item["title"])
            
            tags_html = ""
            for tag in item["tags"]:
                tags_html += "<span class='tag'>{}</span>".format(tag)

            item_html = item_html.replace("{tags}", tags_html)

            if "blurb" in item:
                item_html = item_html.replace("{blurb}", item["blurb"])

            html_snippets.append(item_html)
            
        return html_snippets

def _check_theme_files(theme_directory):
    if not os.path.isfile("{}/{}".format(theme_directory, LAYOUT_FILE_NAME)):
        print("Theme is missing layout file {}".format(LAYOUT_FILE_NAME))
        return False
    
    if not os.path.isfile("{}/{}".format(theme_directory, SNIPPET_FILE_NAME)):
        print("Theme is missing snippet file {}".format(SNIPPET_FILE_NAME))
        return False
    
    return True