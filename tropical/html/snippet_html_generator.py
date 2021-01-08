from tropical.constants import THEME_DIRECTORY_NAME, SNIPPET_FILE_NAME, TAGS_DIRECTORY

class SnippetHtmlGenerator:
    def __init__(self, project_directory):
        # snippet HTML
        with open("{}/{}/{}".format(project_directory, THEME_DIRECTORY_NAME, SNIPPET_FILE_NAME), 'r') as file_pointer:
            self._snippets_template = file_pointer.read()

    def get_snippets_html(self, content_json):
        """Get the HTML snippets for all content items."""
        html_snippets = []

        for item in content_json:
            item_html = self.get_snippet_html(item)
            html_snippets.append(item_html)
            
        return html_snippets

    # item is a dictionary of item attributes e.g. { "title": ..., "url": ...}
    # NB: keep in synch with search.html (JS rendering)
    def get_snippet_html(self, item):
        """Generate the actual HTML for a single snippet."""
        item_html = self._snippets_template
        item_html = item_html.replace("{title}", "<a href='{}'>{}</a>".format(item["url"], item["title"]))
        item_html = item_html.replace("{url}", "<a href='{}'>{}</a>".format(item["url"], item["url"]))

        tags_html = ""
        for tag in item["tags"]:
            tags_html += "<span class='tag'><a href='/{}/{}.html'>{}</a></span>".format(TAGS_DIRECTORY, tag, tag)

        item_html = item_html.replace("{tags}", tags_html)

        item_html = item_html.replace("{blurb}", item["blurb"])
        return item_html

    # We embed this in a single-quoted script in JS, so replace all single-quotes with double-quotes. And minify, sort of.
    def get_snippet_template_for_javascript(self):
        html = self._snippets_template.replace("'", '"').replace("  ", "").replace("\n", "").replace("\r", "")
        snippet_script = "<script type='text/javascript'>window.snippet='{}';</script>".format(html)
        return snippet_script
        
def get_snippets_tagged_with(content_data, target_tag):
    """Find all snippets with a given tag (case-insensitive)"""
    related_items = []

    for item in content_data:
        for tag in item["tags"]:
            normalized_tag = tag.lower()
            if normalized_tag == target_tag.lower():
                related_items.append(item)
                break
    
    return related_items

