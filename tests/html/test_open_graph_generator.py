from tropical.html.open_graph_generator import OpenGraphGenerator
import unittest

class TestOpenGraphGenerator(unittest.TestCase):
    def test_add_meta_tags_adds_meta_tags_with_substitutions(self):
        # Arrange
        config = {
            "siteRootUrl": "https://nightblade9.github.io/game-design-library",
            "openGraph": {
                "title": "Game Design Library",
                "image": "images/open-graph.png",
                "description": "A library of game-design articles that deal with topics like lives, balancing difficulty, perfecting your core loop, loot-boxes, and player experience - without the minutae of game development. Updated weekly."
            }
        }

        expected_title_tag = '<meta property="og:title" content="About - Game Design Library" />'
        expected_type_tag = '<meta property="og:type" content="website" />'
        expected_image_tag = '<meta property="og:image" content="https://nightblade9.github.io/game-design-library/images/open-graph.png" />'
        expected_url_tag = '<meta property="og:url" content="https://nightblade9.github.io/game-design-library" />'
        expected_description_tag = '<meta property="og:description" content="A library of game-design articles that deal with topics like lives, balancing difficulty, perfecting your core loop, loot-boxes, and player experience - without the minutae of game development. Updated weekly." />'

        open_graph = OpenGraphGenerator(config)
        
        # Act
        output = open_graph.add_meta_tags("<head></head>", "About")

        # Assert
        self.assertIn(expected_title_tag, output)
        self.assertIn(expected_type_tag, output)
        self.assertIn(expected_image_tag, output)
        self.assertIn(expected_url_tag, output)
        self.assertIn(expected_description_tag, output)