#!/usr/bin/env python3

import asyncio
import sys
sys.path.insert(0, '.')
from test_000_sphinxmcps.fixtures import mcp_test_server, MCPTestClient

async def test():
    async with (
        mcp_test_server() as port,
        MCPTestClient(port) as client
    ):
        await client.initialize()
        response = await client.call_tool('summarize_inventory', {
            'source': '/nonexistent/path.inv'
        })
        print('Response keys:', list(response.keys()))
        print('Result keys:', list(response.get('result', {}).keys()) if 'result' in response else 'No result')
        print('Has isError:', 'isError' in response.get('result', {}))
        if 'result' in response:
            print('isError value:', response['result'].get('isError'))
            if 'content' in response['result']:
                print('Content:', response['result']['content'])

asyncio.run(test())