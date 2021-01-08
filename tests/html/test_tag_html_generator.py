import unittest
import re

from tropical.html import tag_html_generator

class TestTagHtmlGenerator(unittest.TestCase):

    def test_get_html_for_tag_counts_generates_html_correctly(self):
        # Expectations: 1) header, 2) unordered list, 3) list item per tag
        tag_counts = {"JRPG": 37, "accessibility": 13, "monetization": 2}
        actual = tag_html_generator.get_html_for_tag_counts(tag_counts).lower()

        # Just check content, checking order of tags is flaky
        self.assertTrue("<h1>" in actual)
        self.assertTrue("<ul>" in actual)
        num_list_items = len(re.findall('<li>', actual))
        self.assertEqual(num_list_items, 3)

        for tag in tag_counts:
            target_html = "<li><a href='/tags/{}.html'>{}</a>".format(tag.lower(), tag.lower())
            self.assertTrue(target_html in actual) 