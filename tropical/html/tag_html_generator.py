from tropical.constants import TAGS_DIRECTORY

def get_html_for_tag_counts(tag_item_count, config_json):
    """Given a (presumably sorted by count descending) dictionary of tag => num items, return the HTML."""
    root_url = ""

    if "siteRootUrl" in config_json:
        root_url = config_json["siteRootUrl"]

    tag_index_html = "<h1>Items by Tag</h1>\n<ul>\n"
    for tag in tag_item_count:
        # match everywhere we do tag normalization
        clean_tag = tag.replace("'", "").replace(" ", "-")
        tag_index_html += "<li><a href='{}/{}/{}.html'>{}</a> ({} items)</li>".format(root_url, TAGS_DIRECTORY, clean_tag, tag, tag_item_count[tag])

    tag_index_html += "</ul>\n"
    return tag_index_html

def get_html_for_tag(tag, config_json):
    root_url = ""
    if "siteRootUrl" in config_json:
        root_url = config_json["siteRootUrl"]
        
    # extra trailing space allows tags to break/wrap properly on small screens

    # match everywhere we do tag normalization
    clean_tag = tag.replace("'", "").replace(" ", "-")

    return "<span class='tag'><a href='{}/{}/{}.html'>{}</a></span> ".format(root_url, TAGS_DIRECTORY, clean_tag, tag)
