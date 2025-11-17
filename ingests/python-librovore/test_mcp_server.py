#!/usr/bin/env python3
"""
Quick test of the MCP server fuzzy matching functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'sources'))

from sphinxmcps.server import extract_inventory, summarize_inventory

def test_mcp_server_functions():
    """Test the MCP server functions with fuzzy matching."""
    print("=== Testing MCP Server Functions ===\n")
    
    source = "https://sphobjinv.readthedocs.io/en/stable/"
    
    # Test 1: exact matching (default)
    print("1. Testing extract_inventory with exact matching:")
    try:
        result = extract_inventory(source, term="Inventory")
        print(f"   Found {result['object_count']} objects")
        print(f"   Filters: {result.get('filters', 'None')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: fuzzy matching
    print("\n2. Testing extract_inventory with fuzzy matching:")
    try:
        result = extract_inventory(source, term="DataObj", match_mode="fuzzy", fuzzy_threshold=60)
        print(f"   Found {result['object_count']} objects")
        print(f"   Filters: {result.get('filters', 'None')}")
        if result['objects']:
            domain = list(result['objects'].keys())[0]
            examples = result['objects'][domain][:3]
            print(f"   Example matches: {[obj['name'] for obj in examples]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: regex matching
    print("\n3. Testing extract_inventory with regex matching:")
    try:
        result = extract_inventory(source, term="Data.*Obj", match_mode="regex")
        print(f"   Found {result['object_count']} objects")
        print(f"   Filters: {result.get('filters', 'None')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: summarize_inventory with fuzzy
    print("\n4. Testing summarize_inventory with fuzzy matching:")
    try:
        result = summarize_inventory(source, term="DataObj", match_mode="fuzzy", fuzzy_threshold=70)
        lines = result.split('\n')[:10]  # Show first 10 lines
        print("   Summary (first 10 lines):")
        for line in lines:
            print(f"     {line}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_mcp_server_functions()