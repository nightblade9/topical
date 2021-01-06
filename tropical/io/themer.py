#!/usr/bin/python
import json, os, sys
from tropical.constants import THEME_DIRECTORY_NAME, LAYOUT_FILE_NAME, SNIPPET_FILE_NAME, INDEX_FILENAME, TAGS_DIRECTORY
from tropical.constants import STATIC_CONTENT_DIRECTORY, SEARCH_TEMPLATE_FILE, SEARCH_OUTPUT_FILE, SEARCH_FORM_TEMPLATE_FILE

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

        # load layout HTML
        with open("{}/{}/{}".format(self._project_directory, THEME_DIRECTORY_NAME, LAYOUT_FILE_NAME), 'r') as file_pointer:
            self._layout_html = file_pointer.read()

        # load search form HTML
        with open("{}/{}".format(STATIC_CONTENT_DIRECTORY, SEARCH_FORM_TEMPLATE_FILE), 'r') as file_pointer:
            self._search_form_html = file_pointer.read()

    def generate_output(self, content_data, config):
        blurbs = self._get_snippets_html(content_data)

        all_files = {} # filename => content

        # Tag pages
        all_tags = _get_all_tags(content_data)
        num_tags = {} # tag => number
        unqiue_tags = []

        for tag in all_tags:

            is_duplicate = False
            for seen_before in unqiue_tags:
                if seen_before.lower() == tag.lower():
                    is_duplicate = True
                    break
            if not is_duplicate:
                unqiue_tags.append(tag) # preserve case
            
        for tag in unqiue_tags:
            tagged_items = _get_snippets_tagged_with(content_data, tag)

            tagged_snippets_html = ""
            for item in tagged_items:
                tagged_snippets_html += self._get_snippet_html(item)

            tag_content = "<h1>{} items tagged with {}</h1>\n{}".format(len(tagged_items), tag, tagged_snippets_html)
            tag_page = self._apply_layout_html(tag_content, tag)

            all_files["{}/{}.html".format(TAGS_DIRECTORY, tag)] = tag_page
            num_tags[tag] = len(tagged_items)
        
        # /tags/index.html, an index of tag with count, sorted descendingly by count
        sorted_list = sorted(num_tags.items(), key = lambda x: x[1])
        sorted_list.reverse()
        num_tags_in_order = dict(sorted_list)

        tag_index_html = "<h1>Items by Tag</h1>\n<ul>\n"
        for tag in num_tags_in_order:
            tag_index_html += "<li><a href='/{}/{}.html'>{}</a> ({} items)</li>".format(TAGS_DIRECTORY, tag, tag, num_tags_in_order[tag])

        tag_index_html += "</ul>\n"
        tag_index_html = self._apply_layout_html(tag_index_html, "All Tags")
        all_files["{}/{}".format(TAGS_DIRECTORY, INDEX_FILENAME)] = tag_index_html

        # /search.html, partial page content is in static/search.html. Embedded JS.
        search_template_content:str = ""
        with open("{}/{}".format(STATIC_CONTENT_DIRECTORY, SEARCH_TEMPLATE_FILE), 'r') as file_handle:
            search_template_content = file_handle.read()

        # Embed all data into a variable in our search page as window.data. Use original file: simply assigning
        # content_data generates JSON with single-quoted properties, which breaks when we parse it in JS.
        # Sadly, this obliterates all apostrophes in the content. 'Tis a shame.
        json_data:str = str(content_data).replace("'", '"')
        data_script = "<script type='text/javascript'>window.data='{}';</script>".format(json_data)

        search_html = self._apply_layout_html(search_template_content + data_script, "Search", False)
        all_files[SEARCH_OUTPUT_FILE] = search_html
        
        # Static pages, about (TODO), and index last, since it has the summary of stats.
        stats = "{} items across {} tags".format(len(blurbs), len(unqiue_tags))
        
        index_html = ""
        if "intro" in config:
            index_html = config["intro"] + " "
        index_html += stats
        if "intro_suffix" in config:
            index_html += config["intro_suffix"]

        index_html = "{}{}".format(index_html, str.join("\n", blurbs))
        all_files[INDEX_FILENAME] = self._apply_layout_html(index_html, "Home")

        return { "data": all_files, "stats": stats }
    
    def _apply_layout_html(self, content_html, title, add_search_form = True):
        # TODO: site name comes from config
        final_html = self._layout_html.replace("{content}", content_html) \
            .replace("{pageTitle}", title) \
            .replace("{siteName}", "Game Design Library")

        search_html = self._search_form_html
        if not add_search_form:
            search_html = "" # remove from layout

        final_html = final_html.replace("{search}", search_html)

        return final_html

    def _get_snippets_html(self, content_json):
        html_snippets = []

        for item in content_json:
            item_html = self._get_snippet_html(item)
            html_snippets.append(item_html)
            
        return html_snippets

    # item is a dictionary of item attributes
    # NB: keep in synch with search.html (JS rendering)
    def _get_snippet_html(self, item):
        snippets_template = ""

        with open("{}/{}/{}".format(self._project_directory, THEME_DIRECTORY_NAME, SNIPPET_FILE_NAME), 'r') as file_pointer:
            snippets_template = file_pointer.read()
        
        item_html = snippets_template
        item_html = item_html.replace("{title}", "<a href='{}'>{}</a>".format(item["url"], item["title"]))
        item_html = item_html.replace("{url}", "<a href='{}'>{}</a>".format(item["url"], item["url"]))

        tags_html = ""
        for tag in item["tags"]:
            tags_html += "<span class='tag'><a href='/{}/{}.html'>{}</a></span>".format(TAGS_DIRECTORY, tag, tag)

        item_html = item_html.replace("{tags}", tags_html)

        item_html = item_html.replace("{blurb}", item["blurb"])
        return item_html

def _get_all_tags(content_data):
    all_tags = [] # retain original case
    normalized_tags = []

    for item in content_data:
        for tag in item["tags"]:
            normalized_tag = tag.lower()
            if not normalized_tag in normalized_tags:
                all_tags.append(tag)
    
    return all_tags

def _get_snippets_tagged_with(content_data, target_tag):
    related_items = []

    for item in content_data:
        for tag in item["tags"]:
            normalized_tag = tag.lower()
            if normalized_tag == target_tag.lower():
                related_items.append(item)
                break
    
    return related_items

def _check_theme_files(theme_directory):
    if not os.path.isfile("{}/{}".format(theme_directory, LAYOUT_FILE_NAME)):
        print("Theme is missing layout file {}".format(LAYOUT_FILE_NAME))
        return False
    
    if not os.path.isfile("{}/{}".format(theme_directory, SNIPPET_FILE_NAME)):
        print("Theme is missing snippet file {}".format(SNIPPET_FILE_NAME))
        return False
    
    return True