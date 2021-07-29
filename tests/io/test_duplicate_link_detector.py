from os import dup
from tropical.io import duplicate_link_detector
import unittest

class TestDuplicateLinkDetector(unittest.TestCase):
    def test_find_duplicate_links_finds_duplicates_by_url(self):
        game_design_library_url = "https://nightblade9.github.io/game-design-library"

        content = [
            # There's no normalization/canonicalization right now
            {"url": "http://google.ca"},
            {"url": "http://google.ca/"},
            {"url": game_design_library_url},
            {"url": "http://www.google.ca"},
            {"url": "https://google.ca"},
            {"url": game_design_library_url},
        ]

        actual = duplicate_link_detector.find_duplicate_links(content)

        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0], game_design_library_url)