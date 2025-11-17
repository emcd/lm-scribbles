#!/usr/bin/env python3
# vim: set filetype=python fileencoding=utf-8:

''' Test summarize_inventory refactor to use explore. '''

import asyncio
from tests.test_000_sphinxmcps.fixtures import get_test_inventory_path
import sphinxmcps.functions as functions

async def test():
    inventory_path = get_test_inventory_path('sphinxmcps')
    result = await functions.summarize_inventory(inventory_path, term='DataObj')
    print('SUCCESS: summarize_inventory works')
    print(result[:200])

if __name__ == '__main__':
    asyncio.run(test())