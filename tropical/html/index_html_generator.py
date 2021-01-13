import os

from tropical.constants import THEME_DIRECTORY_NAME, INTRO_FILE_NAME

def generate_index_page_html(project_directory, stats, blurbs):
    """Generates the HTML for the index page, including popular tags and stuff."""
    index_html = ""
    
    intro_file_path = "{}/{}/{}".format(project_directory, THEME_DIRECTORY_NAME, INTRO_FILE_NAME)
    if os.path.isfile(intro_file_path):
        with open(intro_file_path, 'r') as file_handle:
            index_html = file_handle.read()

    index_html = index_html.replace("{stats}", "<span class='stats'>{}</span>".format(stats))
    index_html = "{}{}".format(index_html, str.join("\n", blurbs))
    return index_html