import os
import shutil
from tropical.constants import INTRO_FILE_NAME, THEME_DIRECTORY_NAME
import unittest

from tropical.html import index_html_generator

class TestIndexHtmlGenerator(unittest.TestCase):
    def test_generate_index_page_html_includes_intro_file_and_snippets_html(self):
        # Arrange
        intro_file_html = "<h1>Hello, Intro!</h1>"
        project_dir = "testproject"

        _create_project_directory(project_dir, intro_file_html)

        # Act
        snippets_html = ["<p>Snippet one!</p><div class='snippet'>Snippet TWO!</div>", "Snippet 3"]
        actual = index_html_generator.generate_index_page_html(project_dir, "fake statz", snippets_html)

        # Assert
        try:
            self.assertIn(intro_file_html, actual)
            
            for snippet_html in snippets_html:
                self.assertIn(snippet_html, actual)
        finally:
            shutil.rmtree("testproject")

    def test_generate_index_page_html_includes_stats_html(self):
        # Arrange
        intro_file_html = "<p>{stats}</p>"
        stats = "18 pages over 34 tags"
        project_dir = "testproject"

        _create_project_directory(project_dir, intro_file_html)

        # Act
        actual = index_html_generator.generate_index_page_html(project_dir, stats, [])

        # Assert
        try:
            # <p> tag from template, <span> from Tropical
            self.assertIn("<p><span class='stats'>{}</span></p>".format(stats), actual)
        finally:
            shutil.rmtree("testproject")

def _create_project_directory(project_dir, intro_file_html):
    os.mkdir(project_dir)
    os.mkdir("{}/{}".format(project_dir, THEME_DIRECTORY_NAME))
    with open("{}/{}/{}".format(project_dir, THEME_DIRECTORY_NAME, INTRO_FILE_NAME), 'w') as file_handle:
        file_handle.write(intro_file_html)
