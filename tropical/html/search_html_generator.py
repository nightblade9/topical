from tropical.constants import STATIC_CONTENT_DIRECTORY, SEARCH_FORM_TEMPLATE_FILE

def get_search_html():
    """Gets the search form, from our internal HTML files (not user-provided)"""
    # load search form HTML
    with open("{}/{}".format(STATIC_CONTENT_DIRECTORY, SEARCH_FORM_TEMPLATE_FILE), 'r') as file_pointer:
        search_form_html = file_pointer.read()
    
    return search_form_html