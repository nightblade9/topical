import unittest

from tropical.html.snippet_html_generator import SnippetHtmlGenerator

class TestSnippetHtmlGenerator(unittest.TestCase):

    def test_get_snippets_html_gets_all_snippets_html_including_root_url(self):
        # Arrange
        template = "Title: {title}; URL: {url}; Tags: {tags}; Blurb: {blurb}"
        config_json = {"siteRootUrl": "nightblade.comz"}
        snippets = [
            # no icon
            { "title": "GitHub", "url": "https://github.com", "tags": ["unnecessary", "coding"], "blurb": "GitHub blurb" },
            { "title": "Discord", "url": "https://discord.com", "tags": ["unnecessary", "communication"], "blurb": "Disc Blurb" },
            # eye icon
            { "title": "Twitter", "url": "https://twitter.com", "tags": ["unnecessary", "marketing"], "blurb": "Tweetsalot", "icon": "eye" }
        ]

        generator = SnippetHtmlGenerator(template)
        
        # Act
        actual = generator.get_snippets_html(snippets, config_json)

        # Assert
        self.assertEqual(3, len(actual))
        for i in range(len(snippets)):
            snippet = snippets[i]
            actual_html = actual[i]
            self.assertIn("<a href='{}'>{}</a>".format(snippet["url"], snippet["title"]), actual_html)
            self.assertIn("<a href='{}'>{}</a>".format(snippet["url"], snippet["url"]), actual_html)
            self.assertIn(snippet["blurb"], actual_html)
            for tag in snippet["tags"]:
                self.assertIn("<a href='nightblade.comz/tags/{}.html'>{}</a>".format(tag, tag), actual_html)
            
            if "icon" in snippet:
                expected_icon_html = "<img class='icon' src='{}/images/{}.png".format(config_json["siteRootUrl"], snippet["icon"])
                self.assertIn(expected_icon_html, actual_html)

    def test_get_snippet_html_renders_html_correctly_and_no_root_url(self):
            snippet = { "title": "GDL", "url": "https://nightblade9.github.io/game-design-library", "tags": ["game-design", "STATIC website", "Demon's Face"], "blurb": "Game design library!" }
            template = "GDL template: T={title} U={url} Ts={tags} B={blurb}"
            generator = SnippetHtmlGenerator(template)

            actual = generator.get_snippet_html(snippet, {"siteRootUrl": "https://root.site"})

            # Coarse checks, don't want over-flakiness if the template changes
            self.assertIn("<a href='{}'>{}</a>".format(snippet["url"], snippet["title"]), actual)
            self.assertIn("<a href='{}'>{}</a>".format(snippet["url"], snippet["url"]), actual)
            self.assertIn(snippet["blurb"], actual)
            for tag in snippet["tags"]:
                clean_tag = tag.replace(' ', "-").replace("'", "")
                self.assertIn("<a href='https://root.site/tags/{}.html'>{}</a>".format(clean_tag, tag), actual)
 
    def test_get_snippet_template_for_javascript_replaces_quotes_and_wraps_in_script_tag(self):
        # Very coarse test, don't want it to flake out if we change stuff like compressing results
        template = "Title: '{title}'; URL: '{url}'; Tags: '{tags}'; Blurb: '{blurb}'"
        generator = SnippetHtmlGenerator(template)
        actual = generator.get_snippet_template_for_javascript()

        self.assertIn('Title: "{title}"; URL: "{url}"; Tags: "{tags}"; Blurb: "{blurb}"', actual) # check quotes
        # check wrapping
        self.assertTrue(actual.startswith("<script type='text/javascript'"))
        self.assertTrue(actual.endswith("</script>"))
        self.assertGreater(actual.index("window.snippet="), -1)