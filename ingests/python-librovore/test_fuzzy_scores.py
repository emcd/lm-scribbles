#!/usr/bin/env python3
"""Test rapidfuzz scores for mutex search terms."""

import rapidfuzz.fuzz as fuzz

query = 'mutex'
targets = [
    'tyro.conf.create_mutex_group',
    'tyro.conf._mutex_group', 
    'example-14_mutex',
    'tyro._fields.FieldDefinition.mutex_group'
]

print(f"Query: '{query}'")
print("Target similarity scores:")
for target in targets:
    ratio = fuzz.ratio(query.lower(), target.lower())
    print(f"  {target}: {ratio}%")

print(f"\nDefault threshold: 50%")
print("Objects that would match at threshold 50:")
for target in targets:
    ratio = fuzz.ratio(query.lower(), target.lower())
    if ratio >= 50:
        print(f"  ✓ {target}: {ratio}%")
    else:
        print(f"  ✗ {target}: {ratio}%")