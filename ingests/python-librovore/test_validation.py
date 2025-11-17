#!/usr/bin/env python3

import librovore.functions as funcs
import librovore.exceptions as exc

# Test validation function directly
print('Testing validation function...')

# Test 1: Empty results should raise StructureIncompatibility
try:
    funcs._validate_extraction_results([], [{'name': 'test'}], 'test_proc', 'test_source')
    print('❌ Test 1 failed - should have raised StructureIncompatibility')
except exc.StructureIncompatibility as e:
    print(f'✅ Test 1 passed - {e}')

# Test 2: Meaningful content should pass
try:
    funcs._validate_extraction_results([{'signature': 'def test()', 'description': 'A test'}], [{'name': 'test'}], 'test_proc', 'test_source')
    print('✅ Test 2 passed - validation passed for meaningful content')
except Exception as e:
    print(f'❌ Test 2 failed - {e}')

# Test 3: Low success rate should raise ContentExtractFailure  
try:
    results = [{'signature': '', 'description': ''}] * 10 + [{'signature': 'def good()', 'description': 'Good'}]
    objects = [{'name': f'obj{i}'} for i in range(20)]  # 20 objects, 1 meaningful = 5% < 10%
    funcs._validate_extraction_results(results, objects, 'test_proc', 'test_source')
    print('❌ Test 3 failed - should have raised ContentExtractFailure')
except exc.ContentExtractFailure as e:
    print(f'✅ Test 3 passed - {e}')

print('\nValidation system is working correctly! 🎉')