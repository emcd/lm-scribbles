#!/usr/bin/env python3

import asyncio
import sys
sys.path.insert(0, 'sources')

async def test():
    from sphinxmcps import functions
    from sphinxmcps.__main__ import _prepare
    from sphinxmcps.xtnsmgr import initialize_container
    import contextlib
    
    async with contextlib.AsyncExitStack() as exits:
        auxdata = await _prepare(environment=True, exits=exits, logfile=None)
        await initialize_container(auxdata)
        
        inventory_path = 'tests/data/inventories/sphinxmcps/objects.inv'
        result = await functions.summarize_inventory(inventory_path)
        print('Result:')
        print(repr(result))
        print()
        print('Contains "objects":', 'objects' in result)

if __name__ == '__main__':
    asyncio.run(test())