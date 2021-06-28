def get_snippets_tagged_with(content_data, target_tag):
    """Find all snippets with a given tag (case-insensitive)"""
    related_items = []

    for item in content_data:
        for tag in item["tags"]:
            # tag normalization
            normalized_tag = tag.lower().replace("'", "").replace(' ', '-')
            if normalized_tag == target_tag.lower():
                related_items.append(item)
                break
    
    return related_items

def get_snippets_of_type(content_data, target_type):
    """Find all snippets with a given type (case-insensitive)"""
    related_items = []

    for item in content_data:
        if "type" in item:
            type = item["type"]
            # tag normalization
            normalized_type = type.lower().replace("'", "").replace(' ', '-')
            if normalized_type == target_type.lower():
                related_items.append(item)
    
    return related_items