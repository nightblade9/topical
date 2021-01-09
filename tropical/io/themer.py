#!/usr/bin/python
import glob, os, sys
from tropical.constants import THEME_DIRECTORY_NAME, LAYOUT_FILE_NAME, SNIPPET_FILE_NAME, INDEX_FILENAME, TAGS_DIRECTORY
from tropical.constants import STATIC_CONTENT_DIRECTORY, SEARCH_TEMPLATE_FILE
from tropical.constants import SEARCH_OUTPUT_FILE, SEARCH_FORM_TEMPLATE_FILE, PAGES_DIRECTORY, INTRO_FILE_NAME
from tropical.constants import SCRIPT_WRAPPER_HTML

from tropical.content import tag_counter
from tropical.html import tag_html_generator
from tropical.html import snippet_html_generator
from tropical.html.snippet_html_generator import SnippetHtmlGenerator

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

        # TODO: refactor (move), doesn't belong here
        # snippet HTML
        with open("{}/{}/{}".format(project_directory, THEME_DIRECTORY_NAME, SNIPPET_FILE_NAME), 'r') as file_pointer:
            snippets_template = file_pointer.read()
            self._snippet_generator = SnippetHtmlGenerator(snippets_template)

        # load layout HTML
        with open("{}/{}/{}".format(self._project_directory, THEME_DIRECTORY_NAME, LAYOUT_FILE_NAME), 'r') as file_pointer:
            self._layout_html = file_pointer.read()

        # TODO: refactor (extract)
        # load search form HTML
        with open("{}/{}".format(STATIC_CONTENT_DIRECTORY, SEARCH_FORM_TEMPLATE_FILE), 'r') as file_pointer:
            self._search_form_html = file_pointer.read()
        

    def generate_output(self, content_data, config_file):
        blurbs = self._snippet_generator.get_snippets_html(content_data, config_file)
        blurbs.reverse() # favour newer articles over older ones

        all_files = {} # filename => content
        unique_tags:list = tag_counter.get_unique_tags(content_data)

        # Tag pages            
        for tag in unique_tags:
            tagged_items = snippet_html_generator.get_snippets_tagged_with(content_data, tag)

            tagged_snippets_html = ""
            for item in tagged_items:
                tagged_snippets_html += self._snippet_generator.get_snippet_html(item, config_file)

            tag_content = "<h1>{} items tagged with {}</h1>\n{}".format(len(tagged_items), tag, tagged_snippets_html)
            tag_page = self.apply_layout_html(tag_content, tag)

            all_files["{}/{}.html".format(TAGS_DIRECTORY, tag)] = tag_page
        
        # /tags/index.html, an index of tag with count, sorted descendingly by count
        tag_distribution = tag_counter.get_tag_item_count(content_data)
        tag_index_html = tag_html_generator.get_html_for_tag_counts(tag_distribution, config_file)
        tag_index_html = self.apply_layout_html(tag_index_html, "All Tags")
        all_files["{}/{}".format(TAGS_DIRECTORY, INDEX_FILENAME)] = tag_index_html

        # /search.html, partial page content is in static/search.html. Embedded JS.
        search_template_content:str = ""
        with open("{}/{}".format(STATIC_CONTENT_DIRECTORY, SEARCH_TEMPLATE_FILE), 'r') as file_handle:
            search_template_content = file_handle.read()

        # Embed all data into a variable in our search page as window.data. Use original file: simply assigning
        # content_data generates JSON with single-quoted properties, which breaks when we parse it in JS.
        # Sadly, this obliterates all apostrophes in the content. 'Tis a shame.
        json_data:str = str(content_data).replace("'", '"')
        data_script = SCRIPT_WRAPPER_HTML.format("data", json_data)

        # Also a shame: blurb is user-controlled but search JS is not ... so embed the snippet HTML.
        snippet_html = self._snippet_generator.get_snippet_template_for_javascript()

        # But wait, there's more! Inject the config file in case we need it (e.g. siteRootUrl)
        config_script = SCRIPT_WRAPPER_HTML.format("config", str(config_file).replace("'", '"'))

        search_html = self.apply_layout_html(search_template_content + data_script + snippet_html + config_script, "Search", False)
        all_files[SEARCH_OUTPUT_FILE] = search_html

        # Copy user-made pages
        for filename in glob.glob("{}/{}/*.html".format(self._project_directory, PAGES_DIRECTORY)):
            contents = ""

            just_filename = filename[filename.rindex(os.path.sep) + 1 :]
            title = just_filename[0 : just_filename.rindex('.')]
            
            with open(filename, 'r') as file_handle:
                contents = file_handle.read()
            contents = self.apply_layout_html(contents, title)
            all_files[just_filename] = contents
        # Static pages, about (TODO), and index last, since it has the summary of stats.
        stats = "{} items across {} tags".format(len(blurbs), len(unique_tags))
        
        index_html = ""
        intro_file_path = "{}/{}/{}".format(self._project_directory, THEME_DIRECTORY_NAME, INTRO_FILE_NAME)
        if os.path.isfile(intro_file_path):
            with open(intro_file_path, 'r') as file_handle:
                index_html = file_handle.read()

        index_html = index_html.replace("{stats}", stats)
        index_html = "{}{}".format(index_html, str.join("\n", blurbs))
        all_files[INDEX_FILENAME] = self.apply_layout_html(index_html, "Home")

        return { "data": all_files, "stats": stats }
    
    def apply_layout_html(self, content_html, title, add_search_form = True):
        """
        Applies the theme layout to the target HTML.
        Swaps in the specified title.
        Adds a search form to the body, if add_search_form is True.
        """
        final_html = self._layout_html.replace("{content}", content_html) \
            .replace("{pageTitle}", title) \
            .replace("{siteName}", "Game Design Library")

        search_html = self._search_form_html
        if not add_search_form:
            search_html = "" # remove from layout

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