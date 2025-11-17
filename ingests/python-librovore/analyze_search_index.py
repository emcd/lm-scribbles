#!/usr/bin/env python3
import json
import sys

data = json.load(sys.stdin)
print('Keys:', list(data.keys()))
print('Docs count:', len(data.get('docs', [])))
print('First few docs:')
for idx, doc in enumerate(data.get('docs', [])[:5]):
    print(f'  {idx}: {doc}')

print('\nAuthentication-related docs:')
for idx, doc in enumerate(data.get('docs', [])):
    if 'authentication' in str(doc).lower():
        print(f'  {idx}: {doc}')