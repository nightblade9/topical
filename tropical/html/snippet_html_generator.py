from tropical.html import tag_html_generator
from tropical.constants import SCRIPT_WRAPPER_HTML, TAGS_DIRECTORY

class SnippetHtmlGenerator:
    def __init__(self, snippets_template):
        self._snippets_template = snippets_template

    def get_snippets_html(self, content_json, config_json):
        """Get the HTML snippets for all content items."""
        html_snippets = []

        for item in content_json:
            item_html = self.get_snippet_html(item, config_json)
            html_snippets.append(item_html)
            
        return html_snippets

    # item is a dictionary of item attributes e.g. { "title": ..., "url": ...}
    # NB: keep in synch with search.html (JS rendering)
    def get_snippet_html(self, item, config_json):
        """Generate the actual HTML for a single snippet."""
        root_url = ""

        if "siteRootUrl" in config_json:
            root_url = config_json["siteRootUrl"]

        item_html = self._snippets_template
        title_html = "<a href='{}'>{}</a>".format(item["url"], item["title"])

        if "icon" in item:
            title_html += "<img class='icon' src='{}/images/{}.png' />".format(root_url, item["icon"])

        item_html = item_html.replace("{title}", title_html)
        item_html = item_html.replace("{url}", "<a href='{}'>{}</a>".format(item["url"], item["url"]))

        tags_html = ""
        for tag in item["tags"]:
            # The space after tags is crucial, it allows line-breaking (tags go to the next line, not break half-way).
            tags_html += tag_html_generator.get_html_for_tag(tag, config_json)

        item_html = item_html.replace("{tags}", tags_html)

        item_html = item_html.replace("{blurb}", item["blurb"])
        return item_html

    # We embed this in a single-quoted script in JS, so replace all single-quotes with double-quotes. And minify, sort of.
    def get_snippet_template_for_javascript(self):
        html = self._snippets_template.replace("'", '"').replace("  ", "").replace("\n", "").replace("\r", "")
        snippet_script = SCRIPT_WRAPPER_HTML.format("snippet", html)
        return snippet_script
