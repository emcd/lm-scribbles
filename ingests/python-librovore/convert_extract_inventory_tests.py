#!/usr/bin/env python3
# vim: set filetype=python fileencoding=utf-8:

''' Convert extract_inventory tests to use explore function. '''

import re
from pathlib import Path

def convert_extract_inventory_tests():
    test_file = Path(__file__).parent.parent.parent / 'tests' / 'test_000_sphinxmcps' / 'test_300_functions.py'
    
    content = test_file.read_text()
    
    # Pattern to match extract_inventory function calls with parameters
    pattern = r'await module\.extract_inventory\(\s*([^)]+)\s*\)'
    
    def replace_call(match):
        params = match.group(1).strip()
        
        # Parse parameters - handle simple cases first
        if ',' not in params:
            # Just source parameter
            return f'await module.explore(\n        {params}, "", include_documentation = False )'
        
        # Multiple parameters - need to convert to filters DTO
        parts = [p.strip() for p in params.split(',')]
        source = parts[0]
        
        # Build filters parameter list
        filter_params = []
        other_params = []
        
        for part in parts[1:]:
            if '=' in part:
                key, value = part.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                if key in ['domain', 'role', 'term', 'priority', 'match_mode', 'fuzzy_threshold']:
                    if key == 'term':
                        # term becomes the query parameter
                        return f'await module.explore(\n        {source}, {value}, include_documentation = False )'
                    else:
                        filter_params.append(f'{key} = {value}')
                else:
                    other_params.append(part)
        
        if filter_params:
            filters_def = f'_interfaces.Filters( {", ".join(filter_params)} )'
            return f'await module.explore(\n        {source}, "", filters = {filters_def}, include_documentation = False )'
        else:
            return f'await module.explore(\n        {source}, "", include_documentation = False )'
    
    # Replace function calls
    new_content = re.sub(pattern, replace_call, content, flags=re.MULTILINE | re.DOTALL)
    
    # Update assertions for result structure changes
    new_content = new_content.replace("assert 'objects' in result", "assert 'documents' in result")
    new_content = new_content.replace("result[ 'filters' ]", "result[ 'search_metadata' ][ 'filters' ]")
    new_content = new_content.replace("assert 'filters' in result", "assert 'search_metadata' in result")
    
    # Write back
    test_file.write_text(new_content)
    print(f"Converted {test_file}")

if __name__ == '__main__':
    convert_extract_inventory_tests()