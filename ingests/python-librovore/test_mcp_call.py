#!/usr/bin/env python3

import json
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def test_simple_call():
    print("=== TESTING SIMPLE MCP CALL ===")
    try:
        async with stdio_client(
            StdioServerParameters(command='python', args=['-m', 'sphinxmcps', 'serve'])
        ) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Test the simplest tool call - detect
                print("Testing detect tool...")
                result = await session.call_tool("detect", {
                    "source": "https://docs.python.org"
                })
                print(f"Detect result: {result}")
                
                # Test query_inventory with minimal parameters
                print("\nTesting query_inventory with minimal parameters...")
                result = await session.call_tool("query_inventory", {
                    "source": "https://docs.python.org", 
                    "query": "list"
                })
                result_data = json.loads(result.content[0].text)
                print(f"Query inventory result keys: {list(result_data.keys())}")
                print(f"Found {len(result_data.get('documents', []))} objects")
                
    except Exception as e:
        print(f"Error during MCP test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_simple_call())