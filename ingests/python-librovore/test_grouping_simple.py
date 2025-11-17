#!/usr/bin/env python3

import sys
sys.path.insert(0, 'sources')
from sphinxmcps.functions import _group_documents_by_field

# Test data
documents = [
    {'name': 'func1', 'role': 'function', 'domain': 'py', 'priority': '1', 'uri': '/func1', 'dispname': 'func1'},
    {'name': 'class1', 'role': 'class', 'domain': 'py', 'priority': '1', 'uri': '/class1', 'dispname': 'class1'},
    {'name': 'method1', 'role': 'method', 'domain': 'py', 'priority': '0', 'uri': '/method1', 'dispname': 'method1'},
    {'name': 'var1', 'role': 'data', 'domain': 'std', 'priority': '1', 'uri': '/var1', 'dispname': 'var1'},
]

print('=== Test documents ===')
for doc in documents:
    print(f"  {doc['name']}: role={doc['role']}, domain={doc['domain']}, priority={doc['priority']}")
print()

print('=== Grouping by domain ===')
groups_domain = _group_documents_by_field(documents, 'domain')
for group_name, group_docs in groups_domain.items():
    print(f"  {group_name}: {len(group_docs)} objects - {[doc['name'] for doc in group_docs]}")
print()

print('=== Grouping by role ===')
groups_role = _group_documents_by_field(documents, 'role')
for group_name, group_docs in groups_role.items():
    print(f"  {group_name}: {len(group_docs)} objects - {[doc['name'] for doc in group_docs]}")
print()

print('=== Grouping by priority ===')
groups_priority = _group_documents_by_field(documents, 'priority')
for group_name, group_docs in groups_priority.items():
    print(f"  {group_name}: {len(group_docs)} objects - {[doc['name'] for doc in group_docs]}")
print()

print('=== Grouping by non-existent field ===')
groups_missing = _group_documents_by_field(documents, 'missing_field')
for group_name, group_docs in groups_missing.items():
    print(f"  {group_name}: {len(group_docs)} objects - {[doc['name'] for doc in group_docs]}")
print()

print('=== No grouping (None) ===')
groups_none = _group_documents_by_field(documents, None)
print(f"  Groups: {groups_none}")