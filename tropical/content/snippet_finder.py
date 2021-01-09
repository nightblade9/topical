def get_snippets_tagged_with(content_data, target_tag):
    """Find all snippets with a given tag (case-insensitive)"""
    related_items = []

    for item in content_data:
        for tag in item["tags"]:
            normalized_tag = tag.lower()
            if normalized_tag == target_tag.lower():
                related_items.append(item)
                break
    
    return related_items