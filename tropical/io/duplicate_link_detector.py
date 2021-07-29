#!/usr/bin/python

def find_duplicate_links(content_data:dict):
    links_seen = []
    duplicates = []

    for content in content_data:
        url = content["url"]
        # TODO: normalize and/or use canonical links, e.g. google.com == google.com/ == www.google.com
        if url in links_seen:
            duplicates.append(url)
        else:
            links_seen.append(url)
    
    return duplicates
    