import unittest

from tropical.content import snippet_finder

class TestSnippetFinder(unittest.TestCase):

    def test_get_snippets_tagged_with_gets_snippets_case_insensitively(self):
        # Arrange
        first_snippet = { "tags": ["JRPG", "core-game loop", "Battle"] }
        second_snippet = { "tags": ["Core Game Loop", "platformer"] }
        third_snippet = { "tags": ["monetization"] }

        data = [ first_snippet, second_snippet, third_snippet ]

        # Act
        # normalized value
        actual = snippet_finder.get_snippets_tagged_with(data, "CORE-game-loop")

        # Assert
        self.assertEqual(len(actual), 2)
        self.assertIn(first_snippet, actual)
        self.assertIn(second_snippet, actual)
    
    def test_get_snippets_of_type_gets_snippets_case_insensitively(self):
        # Arrange
        first_snippet = { "type": "VIDEO" }
        second_snippet = { "type": "vidEo" }
        third_snippet = { "type": "article" }

        data = [first_snippet, second_snippet, third_snippet]

        # Act
        actual = snippet_finder.get_snippets_of_type(data, "ViDeo")
        
        # Assert
        self.assertEqual(len(actual), 2)
        self.assertIn(first_snippet, actual)
        self.assertIn(second_snippet, actual)
