from tropical.constants import STATIC_CONTENT_DIRECTORY, SEARCH_FORM_TEMPLATE_FILE
from tropical.constants import SEARCH_TEMPLATE_FILE, STATIC_CONTENT_DIRECTORY, SCRIPT_WRAPPER_HTML

def get_search_form_html(root_url):
    """Gets the search form, from our internal HTML files (not user-provided)"""
    # load search form HTML
    with open("{}/{}".format(STATIC_CONTENT_DIRECTORY, SEARCH_FORM_TEMPLATE_FILE), 'r') as file_pointer:
        search_form_html = file_pointer.read()
    
    search_form_html = search_form_html.replace("{siteRootUrl}", root_url)
    return search_form_html

def generate_search_page_html(content_data, config_json,snippet_generator, themer):
    # /search.html, partial page content is in static/search.html. Embedded JS.
    search_template_content:str = ""
    with open("{}/{}".format(STATIC_CONTENT_DIRECTORY, SEARCH_TEMPLATE_FILE), 'r') as file_handle:
        search_template_content = file_handle.read()

    # Embed all data into a variable in our search page as window.data. Use original file: simply assigning
    # content_data generates JSON with single-quoted properties, which breaks when we parse it in JS.
    # We need to preserve apostrophes IN content, so it doesn't obliterate HTML ...
    for item in content_data:
        item["title"] = item["title"].replace("'", "@@@")

        clean_tags = []
        for tag in item["tags"]:
            # Rules have to match tag-generator and tag filename generation
            clean_tags.append(tag.replace("'", "@@@").replace(' ', '-').replace("'", ''))
        item["tags"] = clean_tags
        
        if "blurb" in item:
            item["blurb"] = item["blurb"].replace("'", "@@@")
    # Convert attribute quoting e.g. 'title' to "title" but preserve apostrophes
    json_data:str = str(content_data).replace("'", '\"').replace('@@@', "\\'")

    data_script = SCRIPT_WRAPPER_HTML.format("data", json_data)

    # Also a shame: blurb is user-controlled but search JS is not ... so embed the snippet HTML.
    snippet_html = snippet_generator.get_snippet_template_for_javascript()

    # But wait, there's more! Inject the config file in case we need it (e.g. siteRootUrl)
    config_script = SCRIPT_WRAPPER_HTML.format("config", str(config_json).replace("'", '"'))

    search_html = themer.apply_layout_html(search_template_content + data_script + snippet_html + config_script, "Search", config_json, False)
    return search_html