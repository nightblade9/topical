import unittest

from tropical.content import tag_finder

class TestTagCounter(unittest.TestCase):

    def test_get_unique_tags_gets_unique_tags_case_insensitively(self):
        data = [
            {
                "tags": ["JrPg", "combat"]
            },
            {
                "tags": ["JRPG", "game balancing"],
            },
            {
                "tags": ["COMBAT", "avacados"]
            }
        ]

        actual = tag_finder.get_unique_tags(data)

        self.assertEqual(4, len(actual))
        self.assertIn("JrPg", actual) # first case is the one returned
        self.assertIn("combat", actual)
        self.assertIn("game balancing", actual)
        self.assertIn("avacados", actual)

    def test_get_tag_item_count_counts_case_insensitively_but_preserves_tag_case(self):
        data = [
            {
                "tags": ["JRPG", "combat"]
            },
            {
                "tags": ["jrpg", "game balancing"],
            },
            {
                "tags": ["COMBAT", "GAME balancing", "JRPG"]
            }
        ]
        
        actual = tag_finder.get_tag_item_count(data)
        self.assertEqual(3, len(actual))
        self.assertEqual(actual["JRPG"], 3) # first one is best boi
        self.assertEqual(actual["combat"], 2)
        self.assertEqual(actual["game balancing"], 2)