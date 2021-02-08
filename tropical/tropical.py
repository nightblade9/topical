#!/usr/bin/python

import glob, json, os, sys, time
from tropical.constants import OUTPUT_DIRECTORY, TAGS_DIRECTORY, THEME_DIRECTORY_NAME, TAGS_METADATA_FILENAME

# all imports related to generate_output
from tropical.constants import INDEX_FILENAME, TAGS_DIRECTORY, SEARCH_OUTPUT_FILE, PAGES_DIRECTORY
from tropical.constants import SNIPPET_FILE_NAME
from tropical.content import tag_finder

from tropical.html import index_html_generator, tag_page_html_generator
from tropical.html.open_graph_generator import OpenGraphGenerator
from tropical.html import search_html_generator
from tropical.html import tag_html_generator
from tropical.html.snippet_html_generator import SnippetHtmlGenerator
from tropical.io.project_manager import ProjectManager
from tropical.io import project_manager
from tropical.io.themer import Themer
from tropical.io import config_fetcher


class Tropical:
    def run(self, args):
        if len(args) < 2:
            print("Usage: python main.py <tropical project directory> [--localhost] [--report-missing-tag-descriptions]")
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
        if "--localhost" in args:
            config_json["siteRootUrl"] = "http://localhost:8000"
            print("Overwriting configured site root URL with localhost:8000")

        report_missing_tag_descriptions = "--report-missing-tag-descriptions" in args
        all_files, stats = self._generate_output(project_directory, content_data, config_json, report_missing_tag_descriptions)

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

    def _generate_output(self, project_directory, content_data, config_json, report_missing_tag_descriptions):
        themer = Themer(project_directory) # validate theme directory and HTML

        # Painfully, has to be applied item by item, because of the prefix/description.
        open_graph = OpenGraphGenerator(config_json)

        snippets_html:list = self._snippet_generator.get_snippets_html(content_data, config_json)
        snippets_html.reverse() # favour newer articles over older ones

        all_files = {} # filename => content
        unique_tags:list = tag_finder.get_unique_tags(content_data)
        tags_metadata = _get_normalized_tags_metadata(project_directory)

        tags_without_descriptions = []
        if report_missing_tag_descriptions:
            tags_without_descriptions = _find_tags_without_descriptions(unique_tags, tags_metadata)

        # Tag pages            
        for tag in unique_tags:
            # match everywhere else we use tag normalization
            normalized_tag = tag.replace(' ', '-').replace("'", "")
            tag_page_html = tag_page_html_generator.generate_tag_page(tag, normalized_tag, self._snippet_generator, content_data, config_json, tags_metadata, themer)
            tag_page_html = open_graph.add_meta_tags(tag_page_html, "Items tagged with {}".format(tag))
            all_files["{}/{}.html".format(TAGS_DIRECTORY, normalized_tag)] = tag_page_html

            if normalized_tag in tags_metadata:
                tags_metadata.pop(normalized_tag)
        
        if len(tags_metadata) > 0:
            unused_tags = ", ".join(tags_metadata.keys())
            print("Warning: there are {} tag(s) in {} that aren't used in any items: {}".format(len(tags_metadata), TAGS_METADATA_FILENAME, unused_tags))
        
        if len(tags_without_descriptions) > 0:
            print("Warning: there are {} tag(s) without metadata descriptions: {}".format(len(tags_without_descriptions), tags_without_descriptions))

        # /tags/index.html, an index of tag with count, sorted descendingly by count
        tag_distribution = tag_finder.get_tag_item_count(content_data)
        tag_index_html = tag_html_generator.get_html_for_tag_counts(tag_distribution, config_json)
        tag_index_html = themer.apply_layout_html(tag_index_html, "All Tags", config_json)
        tag_index_html = open_graph.add_meta_tags(tag_index_html, "All Tags")
        all_files["{}/{}".format(TAGS_DIRECTORY, INDEX_FILENAME)] = tag_index_html
        
        search_html = search_html_generator.generate_search_page_html(content_data, config_json, self._snippet_generator, themer)
        search_html = open_graph.add_meta_tags(search_html, "Search")
        all_files[SEARCH_OUTPUT_FILE] = search_html

        self._generate_user_made_pages(project_directory, config_json, themer, open_graph, all_files)

        # Static pages: index last, since it displays stats
        stats = "{} items across {} tags".format(len(snippets_html), len(unique_tags))

        index_html = index_html_generator.generate_index_page_html(project_directory, stats, snippets_html, tag_distribution, config_json)
        final_html = themer.apply_layout_html(index_html, "", config_json)
        final_html = open_graph.add_meta_tags(final_html, "")
        all_files[INDEX_FILENAME] = final_html

        return [all_files, stats]
    
    def _generate_user_made_pages(self, project_directory, config_json, themer, open_graph, all_files):
        for filename in glob.glob("{}/{}/*.html".format(project_directory, PAGES_DIRECTORY)):
            contents = ""

            just_filename = filename[filename.rindex(os.path.sep) + 1 :]
            title = just_filename[0 : just_filename.rindex('.')]
            title = title[0].upper() + title[1:]
            
            with open(filename, 'r') as file_handle:
                contents = file_handle.read()

            contents = themer.apply_layout_html(contents, title, config_json)
            contents = open_graph.add_meta_tags(contents, title)
            all_files[just_filename] = contents

def _get_normalized_tags_metadata(project_directory):
    # Tags metadata, typically from tags.json. Remove 'em as we go so we can warn about unused metadata.
    tags_json = {}

    tags_metadata_file = "{}/{}".format(project_directory, TAGS_METADATA_FILENAME)
    if os.path.isfile(tags_metadata_file):
        with open(tags_metadata_file) as file_pointer:
            tags_json = json.loads(file_pointer.read())
    
    normalized_tags = {}
    for tag in tags_json.keys():
        # match everywhere else we use tag normalization
        normalized_tag = tag.replace(' ', '-').replace("'", "")
        normalized_tags[normalized_tag] = tags_json[tag]

    return normalized_tags

def _find_tags_without_descriptions(unique_tags, tags_metadata):
    missing_descriptions = unique_tags[:]

    for tag in tags_metadata:
        # match everywhere else we use tag normalization
        normalized_tag = tag.replace(' ', '-').replace("'", "").lower()
        if normalized_tag in unique_tags:
            missing_descriptions.remove(normalized_tag)
    
    return missing_descriptions