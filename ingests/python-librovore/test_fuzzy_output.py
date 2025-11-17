#!/usr/bin/env python3

import json
import sys
sys.path.insert(0, 'sources')

# Test the main user-facing functions to see if fuzzy_score appears

# Simulate what would be returned from each function
def test_structures():
    print("=== Testing query_inventory structure ===")
    # From query_inventory function around line 159
    obj = {
        'name': 'test_func',
        'role': 'function', 
        'domain': 'py',
        'uri': '/test_func',
        'dispname': 'test_func',
        'fuzzy_score': 85  # This is what comes from processor
    }
    
    # What query_inventory returns (explicit structure)
    document = {
        'name': obj['name'],
        'role': obj['role'],
        'domain': obj.get('domain', ''),
        'uri': obj['uri'],
        'dispname': obj['dispname'],
    }
    print("query_inventory document:", json.dumps(document, indent=2))
    print("Contains fuzzy_score:", 'fuzzy_score' in document)
    print()
    
    print("=== Testing _create_document_metadata ===")
    from sphinxmcps.functions import _create_document_metadata
    document2 = _create_document_metadata(obj)
    print("_create_document_metadata result:", json.dumps(document2, indent=2))
    print("Contains fuzzy_score:", 'fuzzy_score' in document2)
    print()
    
    print("=== Testing grouping function ===")
    from sphinxmcps.functions import _group_documents_by_field
    
    # Simulate document as it would come from query_inventory
    doc_for_grouping = _create_document_metadata(obj)
    groups = _group_documents_by_field([doc_for_grouping], 'role')
    print("Grouped result:", json.dumps(groups, indent=2))
    
    if groups:
        first_group = list(groups.values())[0]
        if first_group:
            print("First grouped object contains fuzzy_score:", 'fuzzy_score' in first_group[0])

if __name__ == '__main__':
    test_structures()