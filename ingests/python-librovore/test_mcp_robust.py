#!/usr/bin/env python3

import json
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
# from mcp.types import McpError  # Not available in this version

async def test_robust_calls():
    print("=== ROBUST MCP SERVER TEST ===")
    try:
        async with stdio_client(
            StdioServerParameters(command='python', args=['-m', 'sphinxmcps', 'serve'])
        ) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Test detect - should always work
                print("1. Testing detect tool...")
                try:
                    result = await session.call_tool("detect", {
                        "source": "https://docs.python.org"
                    })
                    print(f"✅ Detect successful")
                except Exception as e:
                    print(f"❌ Detect failed: {e}")
                
                # Test query_inventory that should succeed
                print("2. Testing query_inventory with valid query...")
                try:
                    result = await session.call_tool("query_inventory", {
                        "source": "https://docs.python.org",
                        "query": "str",  # This should find something
                        "results_max": 3
                    })
                    if result.isError:
                        print(f"❌ Query inventory returned error: {result.content}")
                    else:
                        result_data = json.loads(result.content[0].text)
                        print(f"✅ Query inventory successful: found {len(result_data.get('documents', []))} results")
                except Exception as e:
                    print(f"❌ Query inventory failed: {e}")
                
                # Test query_inventory that might fail gracefully
                print("3. Testing query_inventory with potentially problematic query...")
                try:
                    result = await session.call_tool("query_inventory", {
                        "source": "https://docs.python.org",
                        "query": "xyz_nonexistent_function_name_12345",
                        "results_max": 1
                    })
                    if result.isError:
                        print(f"✅ Query inventory properly returned error: {result.content}")
                    else:
                        result_data = json.loads(result.content[0].text) 
                        print(f"✅ Query inventory successful with {len(result_data.get('documents', []))} results")
                except Exception as e:
                    print(f"❌ Query inventory crashed: {e}")
                
                print("4. MCP server test completed")
                
    except Exception as e:
        print(f"❌ Overall test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_robust_calls())