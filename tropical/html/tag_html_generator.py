from tropical.constants import TAGS_DIRECTORY

def get_html_for_tag_counts(tag_item_count):
    """Given a (presumably sorted by count descending) dictionary of tag => num items, return the HTML."""
    tag_index_html = "<h1>Items by Tag</h1>\n<ul>\n"
    for tag in tag_item_count:
        tag_index_html += "<li><a href='/{}/{}.html'>{}</a> ({} items)</li>".format(TAGS_DIRECTORY, tag, tag, tag_item_count[tag])

    tag_index_html += "</ul>\n"
    return tag_index_html