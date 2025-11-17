#!/usr/bin/env python3
# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

''' Test script to verify enum compatibility with FastMCP and Pydantic. '''

import json
from enum import Enum
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Annotated


class MatchMode(Enum):
    ''' Enum for different matching modes. '''
    EXACT = "exact"
    REGEX = "regex"
    FUZZY = "fuzzy"


def test_enum_tool(
    query: Annotated[
        str,
        Field(description="The search query to execute")
    ],
    mode: Annotated[
        MatchMode,
        Field(description="The matching mode to use for the search")
    ] = MatchMode.EXACT,
    case_sensitive: Annotated[
        bool,
        Field(description="Whether the search should be case sensitive")
    ] = False,
) -> dict[str, str]:
    ''' Test function using an enum parameter.
    
    Args:
        query: The search query to execute
        mode: The matching mode to use (EXACT, REGEX, or FUZZY)
        case_sensitive: Whether to perform case-sensitive matching
        
    Returns:
        A dictionary with test results
    '''
    return {
        "query": query,
        "mode": mode.value,
        "mode_name": mode.name,
        "case_sensitive": str(case_sensitive),
        "result": f"Processed '{query}' using {mode.name} mode"
    }


async def main():
    ''' Test the enum integration with FastMCP. '''
    print("Testing enum compatibility with FastMCP...")
    
    # Create FastMCP instance
    mcp = FastMCP("Enum Test Server")
    
    # Register the tool
    mcp.tool()(test_enum_tool)
    
    # Get the list of registered tools
    tools_list = await mcp.list_tools()
    print(f"\nRegistered tools: {[tool.name for tool in tools_list]}")
    
    # Find our test tool
    test_tool = None
    for tool in tools_list:
        if tool.name == 'test_enum_tool':
            test_tool = tool
            break
    
    if test_tool:
        print("\nGenerated Tool Schema:")
        print(f"Name: {test_tool.name}")
        print(f"Description: {test_tool.description}")
        
        # Print the input schema
        if hasattr(test_tool, 'inputSchema'):
            schema = test_tool.inputSchema
            print(f"\nInput Schema:")
            print(json.dumps(schema, indent=2))
            
            # Test the enum parameter schema specifically
            properties = schema.get('properties', {})
            mode_property = properties.get('mode', {})
            
            print(f"\nEnum parameter 'mode' schema:")
            print(json.dumps(mode_property, indent=2))
            
            # Check if enum values are properly represented
            # The enum values are in the $defs section
            defs = schema.get('$defs', {})
            match_mode_def = defs.get('MatchMode', {})
            enum_values = match_mode_def.get('enum', [])
            print(f"\nEnum values in schema: {enum_values}")
            print(f"Enum title: {match_mode_def.get('title', 'N/A')}")
            print(f"Enum description: {match_mode_def.get('description', 'N/A')}")
            print(f"Enum type: {match_mode_def.get('type', 'N/A')}")
        
        # Test calling the tool via MCP
        print(f"\nTesting tool calls via MCP:")
        
        try:
            # Test with string enum value
            result1 = await mcp.call_tool("test_enum_tool", {
                "query": "test query", 
                "mode": "regex", 
                "case_sensitive": True
            })
            print(f"MCP call with 'regex': {result1}")
        except Exception as e:
            print(f"Error calling tool with 'regex': {e}")
            
        try:
            # Test with default values
            result2 = await mcp.call_tool("test_enum_tool", {
                "query": "another test"
            })
            print(f"MCP call with defaults: {result2}")
        except Exception as e:
            print(f"Error calling tool with defaults: {e}")
            
        try:
            # Test with invalid enum value
            result3 = await mcp.call_tool("test_enum_tool", {
                "query": "test query", 
                "mode": "invalid_mode"
            })
            print(f"MCP call with invalid enum: {result3}")
        except Exception as e:
            print(f"Expected error with invalid enum value: {e}")
            
        try:
            # Test all valid enum values
            for enum_val in enum_values:
                result = await mcp.call_tool("test_enum_tool", {
                    "query": f"test {enum_val}", 
                    "mode": enum_val
                })
                print(f"MCP call with '{enum_val}': SUCCESS")
        except Exception as e:
            print(f"Error testing valid enum values: {e}")
    
    else:
        print("ERROR: Tool not found in registry!")
    
    # Test calling the function directly
    print(f"\nTesting direct function calls:")
    
    # Test with enum value
    result1 = test_enum_tool("test query", MatchMode.REGEX, True)
    print(f"Direct call with MatchMode.REGEX: {result1}")
    
    # Test with default enum value
    result2 = test_enum_tool("another test")
    print(f"Direct call with default: {result2}")
    
    # Test all enum values
    for mode in MatchMode:
        result = test_enum_tool(f"test {mode.name.lower()}", mode)
        print(f"Test with {mode.name}: {result}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())