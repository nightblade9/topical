import os
import shutil
from tropical.constants import INTRO_FILE_NAME, THEME_DIRECTORY_NAME
import unittest

from tropical.html import index_html_generator

class TestIndexHtmlGenerator(unittest.TestCase):
    def test_generate_index_page_html_includes_intro_file_and_snippets_html_and_stats_html(self):
        # Arrange
        intro = "<h1>Hello, Intro!</h1>"
        intro_file_html = intro + "<p>{stats}</p>"
        stats = "18 pages over 34 tags"
        project_dir = "testproject"

        os.mkdir(project_dir)
        os.mkdir("{}/{}".format(project_dir, THEME_DIRECTORY_NAME))
        with open("{}/{}/{}".format(project_dir, THEME_DIRECTORY_NAME, INTRO_FILE_NAME), 'w') as file_handle:
            file_handle.write(intro_file_html)

        # Act
        snippets_html = ["<p>Snippet one!</p><div class='snippet'>Snippet TWO!</div>", "Snippet 3"]
        actual = index_html_generator.generate_index_page_html(project_dir, stats, snippets_html)

        # Assert
        try:
            self.assertIn(intro, actual)
            
            for snippet_html in snippets_html:
                self.assertIn(snippet_html, actual)
            
            # <p> tag from template, <span> from Tropical
            self.assertIn("<p><span class='stats'>{}</span></p>".format(stats), actual)
        finally:
            shutil.rmtree("testproject")
