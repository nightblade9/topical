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

def _get_all_tags(content_data):
    all_tags = [] # retain original case
    normalized_tags = []

    for item in content_data:
        for tag in item["tags"]:
            normalized_tag = tag.lower()
            if not normalized_tag in normalized_tags:
                all_tags.append(tag)
    
    return all_tags
