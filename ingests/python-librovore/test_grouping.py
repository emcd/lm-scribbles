#!/usr/bin/env python3

import asyncio
import sys
sys.path.insert(0, 'sources')
from sphinxmcps import functions

async def test_grouping():
    inventory_path = 'tests/data/inventories/sphinxmcps/objects.inv'
    
    # Test default grouping (domain)
    result_default = await functions.summarize_inventory(inventory_path)
    print('=== Default grouping (domain) ===')
    print(result_default)
    print()
    
    # Test grouping by role
    result_role = await functions.summarize_inventory(inventory_path, group_by='role')
    print('=== Grouping by role ===')
    print(result_role)
    print()
    
    # Test grouping by priority  
    result_priority = await functions.summarize_inventory(inventory_path, group_by='priority')
    print('=== Grouping by priority ===')
    print(result_priority)

if __name__ == '__main__':
    asyncio.run(test_grouping())