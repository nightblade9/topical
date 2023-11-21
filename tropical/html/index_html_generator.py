import os
import datetime
from tropical.html import tag_html_generator

from tropical.constants import THEME_DIRECTORY_NAME, INTRO_FILE_NAME

def generate_index_page_html(project_directory, stats,  blurbs, tag_distribution, config_json):
    """Generates the HTML for the index page, including popular tags and stuff."""
    index_html = ""
    
    intro_file_path = "{}/{}/{}".format(project_directory, THEME_DIRECTORY_NAME, INTRO_FILE_NAME)
    if os.path.isfile(intro_file_path):
        with open(intro_file_path, 'r') as file_handle:
            index_html = file_handle.read()

    index_html = index_html.replace("{stats}", "<span class='stats'>{}</span>".format(stats))
    index_html = "{}{}".format(index_html, str.join("\n", blurbs))

    index_html = _show_popular_tags(index_html, tag_distribution, config_json)
    index_html = _show_last_updated(index_html)
    index_html = _show_number_of_items(index_html, config_json)

    return index_html

def _show_number_of_items(index_html, config_json):
    if "{itemsOnHomePage}" in index_html:
        index_html = index_html.replace("{itemsOnHomePage}", str(config_json["itemsOnHomePage"]))
    return index_html

def _show_last_updated(index_html):
    """Substitutes the last-updated date into the token {lastUpdated} if present."""
    if "{lastUpdated}" in index_html:
        now = datetime.datetime.now().strftime("%B %d, %Y")
        index_html = index_html.replace("{lastUpdated}", now)
    return index_html

def _show_popular_tags(index_html, tag_distribution, config_json):
    num_tags = 0
    tags_placeholder = ""

    if "{tags:" in index_html:
        start_index = index_html.index("{tags:") + 6
        stop_index = index_html.index("}", start_index)
        substring = index_html[start_index:stop_index]
        
        if not substring.isdigit():
            print("Warning: can't replace {tags:" + substring + "}, " + substring + " isn't an integer")
            return index_html

        num_tags = int(substring)
        if num_tags <= 0:
            print("Warning: can't replace {tags:" + substring + "}, please specify a positive integer")
            return index_html
        
        tags_placeholder = "{tags:" + substring + "}"
    
    if tags_placeholder != "":
        which_tags = list(tag_distribution.keys())[0 : num_tags]
        popular_tags_html = ""

        for tag in which_tags:
            popular_tags_html += tag_html_generator.get_html_for_tag(tag, config_json)

        index_html = index_html.replace(tags_placeholder, popular_tags_html)    
    
    return index_html
