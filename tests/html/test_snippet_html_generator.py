import unittest

from tropical.html import snippet_html_generator
from tropical.html.snippet_html_generator import SnippetHtmlGenerator

class TestSnippetHtmlGenerator(unittest.TestCase):

    def test_get_snippets_tagged_with_gets_snippets_case_insensitively(self):
        first_snippet = { "tags": ["JRPG", "core game loop", "Battle"] }
        second_snippet = { "tags": ["Core Game Loop", "platformer"] }
        third_snippet = { "tags": ["monetization"] }

        data = [ first_snippet, second_snippet, third_snippet ]

        actual = snippet_html_generator.get_snippets_tagged_with(data, "core game loop")

        self.assertEqual(len(actual), 2)
        self.assertIn(first_snippet, actual)
        self.assertIn(second_snippet, actual)
    
    def test_get_snippets_html_gets_all_snippets_html(self):
        template = "Title: {title}; URL: {url}; Tags: {tags}; Blurb: {blurb}"
        snippets = [
            { "title": "GitHub", "url": "https://github.com", "tags": ["unnecessary", "coding"], "blurb": "GitHub blurb" },
            { "title": "Discord", "url": "https://discord.com", "tags": ["unnecessary", "communication"], "blurb": "Disc Blurb" },
            { "title": "Twitter", "url": "https://twitter.com", "tags": ["unnecessary", "marketing"], "blurb": "Tweetsalot" }
        ]

        generator = SnippetHtmlGenerator(template)
        actual = generator.get_snippets_html(snippets)

        self.assertEqual(3, len(actual))
        for i in range(len(snippets)):
            snippet = snippets[i]
            self.assertIn("<a href='{}'>{}</a>".format(snippet["url"], snippet["title"]), actual[i])
            self.assertIn("<a href='{}'>{}</a>".format(snippet["url"], snippet["url"]), actual[i])
            self.assertIn(snippet["blurb"], actual[i])
            for tag in snippet["tags"]:
                self.assertIn("<a href='/tags/{}.html'>{}</a>".format(tag, tag), actual[i])
            