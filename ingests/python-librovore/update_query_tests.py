#!/usr/bin/env python3

import re

# Read the test file
with open('tests/test_000_sphinxmcps/test_300_functions.py', 'r') as f:
    content = f.read()

# Pattern replacements for updating query_documentation tests
replacements = [
    # Change results = await ... to result = await ...  
    (r'(\s+)results = await module\.query_documentation\(', r'\1result = await module.query_documentation('),
    
    # Change assert isinstance(results, list) to assert isinstance(result, dict)
    (r'assert isinstance\( results, list \)', 'assert isinstance( result, dict )'),
    
    # Add basic structure assertions after isinstance check
    (r'assert isinstance\( result, dict \)', 
     'assert isinstance( result, dict )\n    assert \'documents\' in result\n    assert \'search_metadata\' in result'),
    
    # Change for result in results: to for document in result['documents']:
    (r'for result in results:', 'for document in result[ \'documents\' ]:'),
    
    # Update field access patterns in assertions
    (r'assert result\[ \'domain\' \] == \'py\'', 'assert document[ \'domain\' ] == \'py\''),
    (r'assert result\[ \'object_type\' \] == \'function\'', 'assert document[ \'type\' ] == \'function\''),
    (r'assert result\[ \'priority\' \] == \'1\'', 'assert document[ \'priority\' ] == \'1\''),
    (r'assert \'inventory\' in result\[ \'object_name\' \]\.lower\( \)', 'assert \'inventory\' in document[ \'name\' ].lower( )'),
    
    # Update relevance score assertions
    (r'prev_score = results\[ 0 \]\[ \'relevance_score\' \]', 'prev_score = result[ \'documents\' ][ 0 ][ \'relevance_score\' ]'),
    (r'for result in results\[ 1: \]:', 'for document in result[ \'documents\' ][ 1: ]:'),
    (r'assert result\[ \'relevance_score\' \] <= prev_score\s+prev_score = result\[ \'relevance_score\' \]', 
     'assert document[ \'relevance_score\' ] <= prev_score\n            prev_score = document[ \'relevance_score\' ]'),
    
    # Update length checks
    (r'assert len\( results \) <= 3', 'assert len( result[ \'documents\' ] ) <= 3'),
    (r'assert len\( results \) == 0', 'assert len( result[ \'documents\' ] ) == 0'),
    (r'if len\( results \) > 1:', 'if len( result[ \'documents\' ] ) > 1:'),
    
    # Update content_snippet checks
    (r'assert result\[ \'content_snippet\' \] == \'\'', 'assert document[ \'content_snippet\' ] == \'\''),
    (r'assert \'content_snippet\' in result', 'assert \'content_snippet\' in document'),
    
    # Update match_reasons checks  
    (r'assert \'match_reasons\' in result', 'assert \'match_reasons\' in document'),
    (r'assert isinstance\( result\[ \'match_reasons\' \], list \)', 'assert isinstance( document[ \'match_reasons\' ], list )'),
]

# Apply replacements
for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content)

# Write back the updated content
with open('tests/test_000_sphinxmcps/test_300_functions.py', 'w') as f:
    f.write(content)

print("Updated query_documentation tests")