#!/usr/bin/env python3

''' Batch convert remaining extract_inventory tests to explore. '''

import re
from pathlib import Path

def convert_remaining_tests():
    test_file = Path(__file__).parent.parent.parent / 'tests' / 'test_000_sphinxmcps' / 'test_300_functions.py'
    content = test_file.read_text()
    
    # Define conversion patterns for different test types
    conversions = [
        # Simple auto-append test
        {
            'pattern': r'result = await module\.extract_inventory\(\s*inventory_dir\s*\)',
            'replacement': 'result = await module.explore(\n        inventory_dir, "", include_documentation = False )'
        },
        # Regex term tests  
        {
            'pattern': r'result = await module\.extract_inventory\(\s*([^,]+),\s*term\s*=\s*([^,)]+),\s*match_mode\s*=\s*([^,)]+)\s*\)',
            'replacement': r'filters = _interfaces.Filters( match_mode = \3 )\n    result = await module.explore(\n        \1, \2, filters = filters, include_documentation = False )'
        },
        # Fuzzy matching tests
        {
            'pattern': r'result = await module\.extract_inventory\(\s*([^,]+),\s*term\s*=\s*([^,)]+),\s*match_mode\s*=\s*([^,)]+),\s*fuzzy_threshold\s*=\s*([^,)]+)\s*\)',
            'replacement': r'filters = _interfaces.Filters( match_mode = \3, fuzzy_threshold = \4 )\n    result = await module.explore(\n        \1, \2, filters = filters, include_documentation = False )'
        },
        # Priority filter tests
        {
            'pattern': r'result = await module\.extract_inventory\(\s*([^,]+),\s*priority\s*=\s*([^,)]+)\s*\)',
            'replacement': r'filters = _interfaces.Filters( priority = \2 )\n    result = await module.explore(\n        \1, "", filters = filters, include_documentation = False )'
        },
        # Fuzzy with domain filter
        {
            'pattern': r'result = await module\.extract_inventory\(\s*([^,]+),\s*term\s*=\s*([^,)]+),\s*domain\s*=\s*([^,)]+),\s*match_mode\s*=\s*([^,)]+),\s*fuzzy_threshold\s*=\s*([^,)]+)\s*\)',
            'replacement': r'filters = _interfaces.Filters( domain = \3, match_mode = \4, fuzzy_threshold = \5 )\n    result = await module.explore(\n        \1, \2, filters = filters, include_documentation = False )'
        },
        # Multiple priority tests
        {
            'pattern': r'result_0 = await module\.extract_inventory\(\s*([^,]+),\s*priority\s*=\s*([^,)]+)\s*\)',
            'replacement': r'filters_0 = _interfaces.Filters( priority = \2 )\n    result_0 = await module.explore(\n        \1, "", filters = filters_0, include_documentation = False )'
        },
        {
            'pattern': r'result_1 = await module\.extract_inventory\(\s*([^,]+),\s*priority\s*=\s*([^,)]+)\s*\)',
            'replacement': r'filters_1 = _interfaces.Filters( priority = \2 )\n    result_1 = await module.explore(\n        \1, "", filters = filters_1, include_documentation = False )'
        },
        # Priority with domain
        {
            'pattern': r'result = await module\.extract_inventory\(\s*([^,]+),\s*domain\s*=\s*([^,)]+),\s*priority\s*=\s*([^,)]+)\s*\)',
            'replacement': r'filters = _interfaces.Filters( domain = \2, priority = \3 )\n    result = await module.explore(\n        \1, "", filters = filters, include_documentation = False )'
        }
    ]
    
    # Apply conversions
    for conversion in conversions:
        content = re.sub(conversion['pattern'], conversion['replacement'], content)
    
    # Fix remaining manual cases that need specific handling
    # Update result structure assertions
    content = content.replace("assert 'objects' in result", "assert 'documents' in result")
    content = content.replace("result[ 'filters' ]", "result[ 'search_metadata' ][ 'filters' ]")
    content = content.replace("assert 'filters' in result", "assert 'search_metadata' in result")
    
    # Write back
    test_file.write_text(content)
    print(f"Batch converted remaining tests in {test_file}")

if __name__ == '__main__':
    convert_remaining_tests()