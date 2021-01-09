def get_unique_tags(content_data):
    """Iterates through content_data's tags and returns unique ones (case-insensitively)."""
    all_tags = _get_all_tags(content_data)
    unique_tags = []

    for tag in all_tags:
        is_duplicate = False
        for seen_before in unique_tags:
            if seen_before.lower() == tag.lower():
                is_duplicate = True
                break
        if not is_duplicate:
            unique_tags.append(tag) # preserve case
    
    return unique_tags

def get_tag_item_count(content_data):
    """
    Iterates through content_data's tags and returns the distribution of tags with number of articles per tag.
    Note that the result is a sorted dictionary (dictionary created from a sorted list).
    """
    tag_item_count = {} # tag => count
    normalized_to_name = {} # e.g. jrpg => JRPG

    for item in content_data:
        for tag in item["tags"]:
            normalized_tag = tag.lower()

            if not normalized_tag in tag_item_count:
                tag_item_count[normalized_tag] = 0
            tag_item_count[normalized_tag] += 1

            if not normalized_tag in normalized_to_name:
                normalized_to_name[normalized_tag] = tag
    
    original_name_to_count = {}
    for normalized_name in normalized_to_name:
        original_name = normalized_to_name[normalized_name]
        original_name_to_count[original_name] = tag_item_count[normalized_name]
    
    sorted_list = sorted(original_name_to_count.items(), key = lambda x: x[1])
    sorted_list.reverse()
    tag_item_count_in_order = dict(sorted_list)
    
    return tag_item_count_in_order

def _get_all_tags(content_data):
    all_tags = [] # retain original case
    normalized_tags = []

    for item in content_data:
        for tag in item["tags"]:
            normalized_tag = tag.lower()
            if not normalized_tag in normalized_tags:
                all_tags.append(tag)
    
    return all_tags

