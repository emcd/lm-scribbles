#!/usr/bin/env python3

import json
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def check_server(name, command, args):
    print(f'\n=== {name} ===')
    try:
        async with stdio_client(
            StdioServerParameters(command=command, args=args)
        ) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                response = await session.list_tools()
                
                for tool in response.tools:
                    print(f'\nTool: {tool.name}')
                    if hasattr(tool, 'inputSchema') and tool.inputSchema:
                        # Look for optional parameters in schema
                        properties = tool.inputSchema.get('properties', {})
                        required = tool.inputSchema.get('required', [])
                        
                        for param_name, param_schema in properties.items():
                            is_required = param_name in required
                            print(f'  {param_name}: {json.dumps(param_schema)} (required: {is_required})')
    except Exception as e:
        print(f'Error connecting to {name}: {e}')

async def main():
    # Check our server
    await check_server(
        'Sphinx MCP Server', 
        'python', 
        ['-m', 'sphinxmcps', 'serve']
    )
    
    # Check context7 (if available)
    try:
        await check_server(
            'Context7',
            'npx',
            ['-y', '@context7/mcp-server']
        )
    except:
        print('\nContext7 not available')
    
    # Check pyright (if available) 
    try:
        await check_server(
            'Pyright MCP',
            'python',
            ['-m', 'mcp_pyright']
        )
    except:
        print('\nPyright MCP not available')

if __name__ == "__main__":
    asyncio.run(main())