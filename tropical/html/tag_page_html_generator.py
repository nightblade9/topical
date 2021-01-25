from tropical.content import snippet_finder

def generate_tag_page(tag, normalized_tag, snippet_generator, content_data, config_json, tags_metadata, themer):
    tagged_items = snippet_finder.get_snippets_tagged_with(content_data, normalized_tag)
    tagged_items.reverse() # assume newer = more relevant

    tagged_snippets_html = ""
    for item in tagged_items:
        tagged_snippets_html += snippet_generator.get_snippet_html(item, config_json)
    
    metadata_html = ""
    if normalized_tag in tags_metadata:
        metadata_html = "<p><strong>{}:</strong> {}</p>".format(tag, tags_metadata[normalized_tag])

    tag_content = "<h1>{} items tagged with {}</h1>\n{}\n{}".format(len(tagged_items), tag, metadata_html, tagged_snippets_html)
    tag_page_html = themer.apply_layout_html(tag_content, tag, config_json)
    return tag_page_html