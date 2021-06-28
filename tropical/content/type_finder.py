def get_unique_types(content_data):
    """Iterates through content_data's types and returns unique ones (case-insensitively)."""
    all_types = _get_all_types(content_data)
    unique_types = []

    for type in all_types:
        is_duplicate = False
        for seen_before in unique_types:
            # match everywhere else we use type normalization
            normalized_type = type.replace(' ', '-').replace("'", "").lower()
            normalized_before = seen_before.replace(' ', '-').replace("'", "").lower()
            if normalized_before == normalized_type:
                is_duplicate = True
                break
        if not is_duplicate:
            unique_types.append(type) # preserve case, might be important to the user
    
    return unique_types

def _get_all_types(content_data):
    all_types = [] # retain original case
    normalized_types = []

    for item in content_data:
        if "type" in item:
            type = item["type"]
            normalized_type = type.lower()
            if not normalized_type in normalized_types:
                all_types.append(type)
    
    return all_types

