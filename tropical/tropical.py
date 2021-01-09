#!/usr/bin/python

import glob, json, os, shutil, sys, time
from tropical.constants import OUTPUT_DIRECTORY, TAGS_DIRECTORY, THEME_DIRECTORY_NAME, CONFIG_FILE_NAME
from tropical.io.project_validator import ProjectValidator
from tropical.io.themer import Themer

# all imports related to generate_output
from tropical.constants import INDEX_FILENAME, TAGS_DIRECTORY, SEARCH_TEMPLATE_FILE, SEARCH_OUTPUT_FILE, PAGES_DIRECTORY
from tropical.constants import INTRO_FILE_NAME, SCRIPT_WRAPPER_HTML, SNIPPET_FILE_NAME, STATIC_CONTENT_DIRECTORY
from tropical.content import snippet_finder
from tropical.content import tag_finder
from tropical.html import tag_html_generator
from tropical.html.snippet_html_generator import SnippetHtmlGenerator

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
        
        config_json_path = "{}/{}".format(project_directory, CONFIG_FILE_NAME)
        config_json = {}
        if os.path.isfile(config_json_path):
            with open(config_json_path) as file_handle:
                raw_json = file_handle.read()
                config_json = json.loads(raw_json)
        
        # snippet HTML
        with open("{}/{}/{}".format(project_directory, THEME_DIRECTORY_NAME, SNIPPET_FILE_NAME), 'r') as file_pointer:
            snippets_template = file_pointer.read()
            self._snippet_generator = SnippetHtmlGenerator(snippets_template)

        output = self._generate_output(project_directory, content_data, config_json)
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
        # Sadly, this obliterates all apostrophes in the content. 'Tis a shame.
        json_data:str = str(content_data).replace("'", '"')
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

        index_html = index_html.replace("{stats}", stats)
        index_html = "{}{}".format(index_html, str.join("\n", blurbs))
        all_files[INDEX_FILENAME] = themer.apply_layout_html(index_html, "Home", config_json)

        return {"data": all_files, "stats": stats}