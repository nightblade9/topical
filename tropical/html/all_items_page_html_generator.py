def generate_all_items_page_html(snippet_generator, themer, config_json, content_data):
    """Generates the all.html page, if needed."""
    if not "itemsOnHomePage" in config_json:
        return ""

    snippets_html = ""
    content_data.reverse() # assume newer = more relevant

    for item in content_data:
        snippets_html += snippet_generator.get_snippet_html(item, config_json)
    
    snippets_html = themer.apply_layout_html(snippets_html, "All Items", config_json)
    return snippets_html
