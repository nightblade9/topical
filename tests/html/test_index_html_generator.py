import os
import shutil
from tropical.constants import INTRO_FILE_NAME, THEME_DIRECTORY_NAME
import unittest

from tropical.html import index_html_generator, tag_html_generator

class TestIndexHtmlGenerator(unittest.TestCase):
    def test_generate_index_page_html_includes_intro_file_and_snippets_html(self):
        # Arrange
        intro_file_html = "<h1>Hello, Intro!</h1>"
        project_dir = "testproject1"

        _create_project_directory(project_dir, intro_file_html)

        # Act
        snippets_html = ["<p>Snippet one!</p><div class='snippet'>Snippet TWO!</div>", "Snippet 3"]
        actual = index_html_generator.generate_index_page_html(project_dir, "fake statz", snippets_html, {}, {})

        # Assert
        try:
            self.assertIn(intro_file_html, actual)
            
            for snippet_html in snippets_html:
                self.assertIn(snippet_html, actual)
        finally:
            shutil.rmtree(project_dir)

    def test_generate_index_page_html_includes_stats_html(self):
        # Arrange
        intro_file_html = "<p>{stats}</p>"
        stats = "18 pages over 34 tags"
        project_dir = "testproject2"

        _create_project_directory(project_dir, intro_file_html)

        # Act
        actual = index_html_generator.generate_index_page_html(project_dir, stats, [], {}, {})

        # Assert
        try:
            # <p> tag from template, <span> from Tropical
            self.assertIn("<p><span class='stats'>{}</span></p>".format(stats), actual)
        finally:
            shutil.rmtree(project_dir)
    
    def test_generate_index_page_html_adds_specified_number_of_popular_tags(self):
        # Arrange
        intro_file_html = "<p>{tags:2}</p>"
        tag_distribution = {"arpg": 3, "platformer": 2, "idle": 1}
        project_dir = "testproject3"
        _create_project_directory(project_dir, intro_file_html)

        # Act
        config_json = {}
        actual = index_html_generator.generate_index_page_html(project_dir, "", [], tag_distribution, config_json)

        # Assert
        try:
            expected_tags = list(tag_distribution.keys())[0:2]

            for tag in expected_tags:
                expected_html = tag_html_generator.get_html_for_tag(tag, config_json)
                self.assertIn(expected_html, actual)
        finally:
            shutil.rmtree(project_dir)

    def test_generate_index_page_html_does_not_add_adds_popular_tags_if_number_is_invalid(self):
        test_cases = [-1, 0, 2.4, "foo"]
        for n in test_cases:
            with self.subTest(msg="Checking for an invalid number of tags", n=n):
                # Arrange
                tags_specification = "{tags:" + str(n) + "}"
                intro_file_html = "<p>{}</p>".format(tags_specification)
                print(intro_file_html)
                project_dir = "testproject4"

                _create_project_directory(project_dir, intro_file_html)

                # Act
                actual = index_html_generator.generate_index_page_html(project_dir, "no stats", [], {}, {})

                # Assert
                try:
                    self.assertIn(tags_specification, actual) # Wasn't replaced
                finally:
                    if os.path.isdir(project_dir):
                        shutil.rmtree(project_dir)

def _create_project_directory(project_dir, intro_file_html):
    if os.path.isdir(project_dir):
        shutil.rmtree(project_dir)

    os.mkdir(project_dir)
    os.mkdir("{}/{}".format(project_dir, THEME_DIRECTORY_NAME))
    with open("{}/{}/{}".format(project_dir, THEME_DIRECTORY_NAME, INTRO_FILE_NAME), 'w') as file_handle:
        file_handle.write(intro_file_html)
