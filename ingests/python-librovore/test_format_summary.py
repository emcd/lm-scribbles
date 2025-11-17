#!/usr/bin/env python3

import sys
sys.path.insert(0, 'sources')
from sphinxmcps.functions import _format_inventory_summary

# Test data for grouped format (dict)
grouped_data = {
    'project': 'Test Project',
    'version': '1.0.0',
    'object_count': 4,
    'objects': {
        'py': [
            {'name': 'func1', 'role': 'function', 'domain': 'py', 'uri': '/func1', 'dispname': 'func1'},
            {'name': 'class1', 'role': 'class', 'domain': 'py', 'uri': '/class1', 'dispname': 'class1'},
        ],
        'std': [
            {'name': 'var1', 'role': 'data', 'domain': 'std', 'uri': '/var1', 'dispname': 'var1'},
        ],
        '(missing domain)': [
            {'name': 'orphan1', 'role': 'method', 'uri': '/orphan1', 'dispname': 'orphan1'},
        ]
    },
    'filters': {'role': 'function'}
}

# Test data for ungrouped format (list)
ungrouped_data = {
    'project': 'Test Project',
    'version': '1.0.0', 
    'object_count': 7,
    'objects': [
        {'name': 'func1', 'role': 'function', 'domain': 'py', 'uri': '/func1', 'dispname': 'func1'},
        {'name': 'class1', 'role': 'class', 'domain': 'py', 'uri': '/class1', 'dispname': 'class1'},
        {'name': 'method1', 'role': 'method', 'domain': 'py', 'uri': '/method1', 'dispname': 'method1'},
        {'name': 'var1', 'role': 'data', 'domain': 'std', 'uri': '/var1', 'dispname': 'var1'},
        {'name': 'var2', 'role': 'data', 'domain': 'std', 'uri': '/var2', 'dispname': 'var2'},
        {'name': 'func2', 'role': 'function', 'domain': 'py', 'uri': '/func2', 'dispname': 'func2'},
        {'name': 'attr1', 'role': 'attribute', 'domain': 'py', 'uri': '/attr1', 'dispname': 'attr1'},
    ],
    'filters': {}
}

print('=== Test 1: Grouped format (with domain grouping) ===')
result = _format_inventory_summary(grouped_data)
print(result)
print()

print('=== Test 2: Ungrouped format (flat list) ===')
result = _format_inventory_summary(ungrouped_data)
print(result)
print()

print('=== Test 3: Empty objects ===')
empty_data = {
    'project': 'Empty Project',
    'version': '1.0.0',
    'object_count': 0,
    'objects': [],
    'filters': {}
}
result = _format_inventory_summary(empty_data)
print(result)