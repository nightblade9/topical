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

    # Embed snippet template into a variable in our search page as window.snippet.
    # blurb template is user-controlled but search JS is not ... so embed the snippet HTML.
    snippet_html = snippet_generator.get_snippet_template_for_javascript()

    # But wait, there's more! Inject the config file in case we need it (e.g. siteRootUrl)
    # window.config = config_json
    config_script = SCRIPT_WRAPPER_HTML.format("config", str(config_json).replace("'", '"'))

    search_html = themer.apply_layout_html(search_template_content + snippet_html + config_script, "Search", config_json, False)
    return search_html