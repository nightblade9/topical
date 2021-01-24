from tropical.html import search_html_generator
import unittest

class TestSearchHtmlGenerator(unittest.TestCase):
    def test_get_search_form_html_gets_form_html_and_replaces_site_root(self):
        # Arrange
        root_url = "https://gamedesignlibrary.wut/beta"

        # Act
        actual = search_html_generator.get_search_form_html(root_url)

        # Assert
        self.assertIn('action="{}/search.html"'.format(root_url), actual)