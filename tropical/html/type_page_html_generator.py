from tropical.content import snippet_finder
from tropical.constants import TYPES_DIRECTORY

def generate_type_page(type, normalized_type, snippet_generator, content_data, config_json, themer):
    type_items = snippet_finder.get_snippets_of_type(content_data, normalized_type)
    type_items.reverse() # assume newer = more relevant

    typed_snippets_html = ""
    for item in type_items:
        typed_snippets_html += snippet_generator.get_snippet_html(item, config_json)
    
    metadata_html = ""
    type_content = "<h1>{} {} items</h1>\n{}\n{}".format(len(type_items), type, metadata_html, typed_snippets_html)
    type_page_html = themer.apply_layout_html(type_content, type, config_json)
    return type_page_html

# TOOD: move to type_page_generator
def get_link_for(type):
    return "{}/{}.html".format(TYPES_DIRECTORY, type.lower())