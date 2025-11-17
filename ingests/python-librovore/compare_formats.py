#!/usr/bin/env python3

import asyncio
import sys
import json
sys.path.append('tests')
sys.path.insert(0, 'sources')
import sphinxmcps.functions as module
from test_000_sphinxmcps.fixtures import get_test_inventory_path

async def test():
    inventory_path = get_test_inventory_path('sphobjinv')
    
    print("=== EXPLORE FORMAT ===")
    explore_result = await module.explore(inventory_path, 'inventory', max_objects=2)
    print(json.dumps(explore_result, indent=2, default=str))
    
    print("\n=== QUERY_DOCUMENTATION FORMAT ===")
    query_result = await module.query_documentation(inventory_path, 'inventory', max_results=2)
    print(json.dumps(query_result, indent=2, default=str))

if __name__ == '__main__':
    asyncio.run(test())