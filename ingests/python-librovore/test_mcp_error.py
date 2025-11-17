#!/usr/bin/env python3

import asyncio
import sys
sys.path.insert(0, 'sources')
import sphinxmcps.server as module

async def test():
    try:
        result = await module.explore('/nonexistent/path.inv', 'test')
        print('Result:', result)
        print('Has error key:', 'error' in result)
        if 'error' in result:
            print('Error message:', result['error'])
    except Exception as e:
        print('Exception caught:', type(e), str(e))

if __name__ == '__main__':
    asyncio.run(test())