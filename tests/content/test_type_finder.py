import unittest

from tropical.content import type_finder

class TestTagCounter(unittest.TestCase):

    def test_get_unique_tags_gets_unique_tags_case_insensitively_but_preserves_case(self):
        # Arrange
        first_snippet = { "type": "VIDEO" }
        second_snippet = { "type": "vidEo" }
        third_snippet = { "type": "article" }

        data = [first_snippet, second_snippet, third_snippet]

        actual = type_finder.get_unique_types(data)

        self.assertEqual(2, len(actual))
        self.assertIn("VIDEO", actual) # first case is the one returned