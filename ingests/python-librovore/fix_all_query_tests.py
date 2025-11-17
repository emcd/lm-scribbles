#!/usr/bin/env python3

import re

# Read the test file
with open('tests/test_000_sphinxmcps/test_300_functions.py', 'r') as f:
    content = f.read()

# Define a comprehensive set of transformations
transformations = [
    # Fix function calls with old-style parameters
    (r'results = await module\.query_documentation\(\s*([^,]+),\s*([^,]+),\s*match_mode = ([^)]+)\s*\)',
     r'filters = _interfaces.Filters( match_mode = \3 )\n    result = await module.query_documentation(\1, \2, filters = filters )'),
    
    (r'results = await module\.query_documentation\(\s*([^,]+),\s*([^,]+),\s*fuzzy_threshold = ([^)]+)\s*\)',
     r'filters = _interfaces.Filters( fuzzy_threshold = \3 )\n    result = await module.query_documentation(\1, \2, filters = filters )'),
    
    (r'results = await module\.query_documentation\(\s*([^,]+),\s*([^,]+),\s*max_results = ([^)]+)\s*\)',
     r'result = await module.query_documentation(\1, \2, max_results = \3 )'),
    
    (r'results = await module\.query_documentation\(\s*([^,]+),\s*([^,]+),\s*include_snippets = ([^)]+)\s*\)',
     r'result = await module.query_documentation(\1, \2, include_snippets = \3 )'),
    
    # Fix complex calls with multiple parameters
    (r'results = await module\.query_documentation\(\s*([^,]+),\s*([^,]+),\s*match_mode = ([^,]+),\s*fuzzy_threshold = ([^)]+)\s*\)',
     r'filters = _interfaces.Filters( match_mode = \3, fuzzy_threshold = \4 )\n    result = await module.query_documentation(\1, \2, filters = filters )'),
    
    # Fix assert statements
    (r'assert isinstance\( results, list \)', 
     'assert isinstance( result, dict )\n    assert \'documents\' in result'),
    
    # Fix loop iterations
    (r'for result in results:', 'for document in result[ \'documents\' ]:'),
    
    # Fix field access in loops
    (r'assert \'inventory\' in result\[ \'object_name\' \]\.lower\( \)',
     'assert \'inventory\' in document[ \'name\' ].lower( )'),
    
    (r'assert result\[ \'content_snippet\' \] == \'\'',
     'assert document[ \'content_snippet\' ] == \'\''),
    
    (r'assert \'content_snippet\' in result\b',
     'assert \'content_snippet\' in document'),
    
    (r'assert \'match_reasons\' in result\b',
     'assert \'match_reasons\' in document'),
    
    (r'assert isinstance\( result\[ \'match_reasons\' \], list \)',
     'assert isinstance( document[ \'match_reasons\' ], list )'),
    
    # Fix length checks
    (r'assert len\( results \) <= 3', 'assert len( result[ \'documents\' ] ) <= 3'),
    (r'assert len\( results \) == 0', 'assert len( result[ \'documents\' ] ) == 0'),
    (r'if len\( results \) > 1:', 'if len( result[ \'documents\' ] ) > 1:'),
    
    # Fix relevance ranking test
    (r'prev_score = results\[ 0 \]\[ \'relevance_score\' \]',
     'prev_score = result[ \'documents\' ][ 0 ][ \'relevance_score\' ]'),
    (r'for result in results\[ 1: \]:',
     'for document in result[ \'documents\' ][ 1: ]:'),
    (r'assert result\[ \'relevance_score\' \] <= prev_score\s*prev_score = result\[ \'relevance_score\' \]',
     'assert document[ \'relevance_score\' ] <= prev_score\n            prev_score = document[ \'relevance_score\' ]'),
    
    # Fix combined filters test
    (r'results = await module\.query_documentation\(\s*([^,]+),\s*([^,]+),\s*domain = ([^,]+),\s*role = ([^,]+),\s*priority = ([^,]+),\s*match_mode = ([^,]+),\s*fuzzy_threshold = ([^)]+)\s*\)',
     r'filters = _interfaces.Filters( domain = \3, role = \4, priority = \5, match_mode = \6, fuzzy_threshold = \7 )\n    result = await module.query_documentation(\1, \2, filters = filters )'),
    
    # Fix simple calls
    (r'results = await module\.query_documentation\( ([^,]+), ([^)]+) \)',
     r'result = await module.query_documentation( \1, \2 )'),
]

# Apply transformations
for pattern, replacement in transformations:
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

# Fix any remaining structure checks
if 'if results:' in content:
    content = content.replace('if results:', 'if result[ \'documents\' ]:')
    content = content.replace('result = results[ 0 ]', 'document = result[ \'documents\' ][ 0 ]')

# Write back
with open('tests/test_000_sphinxmcps/test_300_functions.py', 'w') as f:
    f.write(content)

print("Fixed all query_documentation tests")