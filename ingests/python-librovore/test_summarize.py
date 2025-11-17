#!/usr/bin/env python3

import asyncio
import sys
sys.path.insert(0, 'sources')
from sphinxmcps import functions

async def test():
    inventory_path = 'tests/data/inventories/sphinxmcps/objects.inv'
    
    print('=== Test 1: No grouping (should show flat list) ===')
    result = await functions.summarize_inventory(inventory_path)
    print(result)
    print()
    
    print('=== Test 2: Group by domain ===')
    result = await functions.summarize_inventory(inventory_path, group_by='domain')
    print(result)
    print()
    
    print('=== Test 3: Group by role ===')
    result = await functions.summarize_inventory(inventory_path, group_by='role')
    print(result)

if __name__ == '__main__':
    asyncio.run(test())