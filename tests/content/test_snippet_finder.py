import unittest

from tropical.content import snippet_finder

class TestSnippetFinder(unittest.TestCase):

    def test_get_snippets_tagged_with_gets_snippets_case_insensitively(self):
        first_snippet = { "tags": ["JRPG", "core-game loop", "Battle"] }
        second_snippet = { "tags": ["Core Game Loop", "platformer"] }
        third_snippet = { "tags": ["monetization"] }

        data = [ first_snippet, second_snippet, third_snippet ]

        # normalized value
        actual = snippet_finder.get_snippets_tagged_with(data, "core-game-loop")

        self.assertEqual(len(actual), 2)
        self.assertIn(first_snippet, actual)
        self.assertIn(second_snippet, actual)
    