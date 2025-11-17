#!/usr/bin/env python3

import asyncio
import sys
sys.path.insert(0, '../sources')
import sphinxmcps.functions as module
from test_000_sphinxmcps.fixtures import get_test_inventory_path

async def test():
    inventory_path = get_test_inventory_path('sphobjinv')
    result = await module.explore(inventory_path, 'nonexistent_object', max_objects=1)
    print('Result keys:', list(result.keys()))
    if 'errors' in result:
        print('Errors:', result['errors'])
    if 'error' in result:
        print('Error:', result['error'])
    if 'documents' in result:
        print('Documents count:', len(result['documents']))
    
    # Print the full result structure
    import json
    print('\nFull result:')
    print(json.dumps(result, indent=2, default=str))

if __name__ == '__main__':
    asyncio.run(test())