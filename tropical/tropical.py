#!/usr/bin/python

import glob, os, sys, time
from tropical.constants import OUTPUT_DIRECTORY, TAGS_DIRECTORY, THEME_DIRECTORY_NAME
from tropical.io.project_manager import ProjectManager
from tropical.io import project_manager
from tropical.io.themer import Themer
from tropical.io import config_fetcher

# all imports related to generate_output
from tropical.constants import INDEX_FILENAME, TAGS_DIRECTORY, SEARCH_TEMPLATE_FILE, SEARCH_OUTPUT_FILE, PAGES_DIRECTORY
from tropical.constants import INTRO_FILE_NAME, SCRIPT_WRAPPER_HTML, SNIPPET_FILE_NAME, STATIC_CONTENT_DIRECTORY
from tropical.content import snippet_finder
from tropical.content import tag_finder
from tropical.html import tag_html_generator
from tropical.html.snippet_html_generator import SnippetHtmlGenerator

class Tropical:
    def run(self, args):
        if len(args) != 2:
            print("Usage: python main.py <tropical project directory>")
            sys.exit(1)

        project_directory = args[1]
        start_time = time.time()
        manager = ProjectManager(project_directory)
        content_data = manager.get_data()
        
        # snippet HTML
        with open("{}/{}/{}".format(project_directory, THEME_DIRECTORY_NAME, SNIPPET_FILE_NAME), 'r') as file_pointer:
            snippets_template = file_pointer.read()
            self._snippet_generator = SnippetHtmlGenerator(snippets_template)
        
        config_json = config_fetcher.get_config(project_directory)

        all_files, stats = self._generate_output(project_directory, content_data, config_json)

        output_directory = "{}/{}".format(project_directory, OUTPUT_DIRECTORY)
        project_manager.recreate_output_directory(output_directory)

        for filename in all_files:
            contents = all_files[filename]
            output_filename = "{}/{}".format(output_directory, filename)

            with open(output_filename, 'w') as file_pointer:
                file_pointer.write(contents)
                file_pointer.close()

        # copy static JS required for tropical functions (search)
        project_manager.copy_required_static_files(output_directory)
        project_manager.copy_theme_files(project_directory, output_directory)
        
        stop_time = time.time()
        
        print("{}, totaling {} pages - generated in {}s".format(stats, len(all_files), (stop_time - start_time)))

    def _generate_output(self, project_directory, content_data, config_json):
        themer = Themer(project_directory) # validate theme directory

        blurbs = self._snippet_generator.get_snippets_html(content_data, config_json)
        blurbs.reverse() # favour newer articles over older ones

        all_files = {} # filename => content
        unique_tags:list = tag_finder.get_unique_tags(content_data)

        # Tag pages            
        for tag in unique_tags:
            tagged_items = snippet_finder.get_snippets_tagged_with(content_data, tag)

            tagged_snippets_html = ""
            for item in tagged_items:
                tagged_snippets_html += self._snippet_generator.get_snippet_html(item, config_json)

            tag_content = "<h1>{} items tagged with {}</h1>\n{}".format(len(tagged_items), tag, tagged_snippets_html)
            tag_page = themer.apply_layout_html(tag_content, tag, config_json)

            all_files["{}/{}.html".format(TAGS_DIRECTORY, tag)] = tag_page
        
        # /tags/index.html, an index of tag with count, sorted descendingly by count
        tag_distribution = tag_finder.get_tag_item_count(content_data)
        tag_index_html = tag_html_generator.get_html_for_tag_counts(tag_distribution, config_json)
        tag_index_html = themer.apply_layout_html(tag_index_html, "All Tags", config_json)
        all_files["{}/{}".format(TAGS_DIRECTORY, INDEX_FILENAME)] = tag_index_html

        # /search.html, partial page content is in static/search.html. Embedded JS.
        search_template_content:str = ""
        with open("{}/{}".format(STATIC_CONTENT_DIRECTORY, SEARCH_TEMPLATE_FILE), 'r') as file_handle:
            search_template_content = file_handle.read()

        # Embed all data into a variable in our search page as window.data. Use original file: simply assigning
        # content_data generates JSON with single-quoted properties, which breaks when we parse it in JS.
        # We need to preserve apostrophes IN content, so it doesn't obliterate HTML ...
        for item in content_data:
            item["title"] = item["title"].replace("'", "@@@")
            if "blurb" in item:
                item["blurb"] = item["blurb"].replace("'", "@@@")
        # Convert attribute quoting e.g. 'title' to "title" but preserve apostrophes
        json_data:str = str(content_data).replace("'", '\"').replace('@@@', "\\'")

        data_script = SCRIPT_WRAPPER_HTML.format("data", json_data)

        # Also a shame: blurb is user-controlled but search JS is not ... so embed the snippet HTML.
        snippet_html = self._snippet_generator.get_snippet_template_for_javascript()

        # But wait, there's more! Inject the config file in case we need it (e.g. siteRootUrl)
        config_script = SCRIPT_WRAPPER_HTML.format("config", str(config_json).replace("'", '"'))

        search_html = themer.apply_layout_html(search_template_content + data_script + snippet_html + config_script, "Search", config_json, False)
        all_files[SEARCH_OUTPUT_FILE] = search_html

        # Copy user-made pages
        for filename in glob.glob("{}/{}/*.html".format(project_directory, PAGES_DIRECTORY)):
            contents = ""

            just_filename = filename[filename.rindex(os.path.sep) + 1 :]
            title = just_filename[0 : just_filename.rindex('.')]
            
            with open(filename, 'r') as file_handle:
                contents = file_handle.read()

            contents = themer.apply_layout_html(contents, title, config_json)
            all_files[just_filename] = contents
        # Static pages, about (TODO), and index last, since it has the summary of stats.
        stats = "{} items across {} tags".format(len(blurbs), len(unique_tags))
        
        index_html = ""
        intro_file_path = "{}/{}/{}".format(project_directory, THEME_DIRECTORY_NAME, INTRO_FILE_NAME)
        if os.path.isfile(intro_file_path):
            with open(intro_file_path, 'r') as file_handle:
                index_html = file_handle.read()

        index_html = index_html.replace("{stats}", "<span class='stats'>{}</span>".format(stats))
        index_html = "{}{}".format(index_html, str.join("\n", blurbs))
        all_files[INDEX_FILENAME] = themer.apply_layout_html(index_html, "Home", config_json)

        return [all_files, stats]