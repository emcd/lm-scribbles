#!/usr/bin/env python3

import json
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def check_schemas():
    print("=== UPDATED SCHEMA TEST ===")
    async with stdio_client(
        StdioServerParameters(command='python', args=['-m', 'sphinxmcps', 'serve'])
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            response = await session.list_tools()
            
            for tool in response.tools:
                print(f'\n=== {tool.name} ===')
                print(f'Description: {tool.description}')
                print(f'Input Schema:')
                schema = tool.inputSchema
                print(json.dumps(schema, indent=2))
                
                # Analyze the optional parameters
                properties = schema.get('properties', {})
                required = schema.get('required', [])
                
                print(f'\nParameter Analysis:')
                for param_name, param_schema in properties.items():
                    is_required = param_name in required
                    param_type = param_schema.get('type', 'unknown')
                    has_anyof = 'anyOf' in param_schema
                    default_val = param_schema.get('default', 'no default')
                    description = param_schema.get('description', 'no description')
                    print(f'  {param_name}: type={param_type}, required={is_required}, anyOf={has_anyof}, default={default_val}, description={description}')

if __name__ == "__main__":
    asyncio.run(check_schemas())