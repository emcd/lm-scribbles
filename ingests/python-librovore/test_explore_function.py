#!/usr/bin/env python3
# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

''' Test the new explore function. '''

import asyncio
import json
from pathlib import Path

# Import the explore function and dependencies
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'sources'))

from sphinxmcps import functions
from sphinxmcps.functions import Filters
from sphinxmcps import interfaces

async def test_explore_function():
    ''' Test the explore function with local inventory. '''
    print("Testing explore function...\n")
    
    # Initialize processors (needed for the function to work)
    from sphinxmcps import xtnsmgr
    from sphinxmcps import appcore
    
    async with appcore.prepare() as auxdata:
        await xtnsmgr.register_processors(auxdata)
        
        # Use local test inventory
        test_inventory = Path(__file__).parent.parent / 'tests' / 'data' / 'inventories' / 'sphinxmcps' / 'objects.inv'
        source = f"file://{test_inventory.absolute()}"
        
        await _run_tests(source)
    
    print(f"Testing with source: {source}\n")
    
    # Test 1: Basic explore with defaults
    print("=== Test 1: Basic explore (defaults) ===")
    try:
        result = await functions.explore(source, "DataObj")
        print(f"✓ SUCCESS: Found {result['search_metadata']['object_count']} objects")
        print(f"  Project: {result['project']}")
        print(f"  Version: {result['version']}")
        print(f"  Total matches: {result['search_metadata']['total_matches']}")
        print(f"  Documents: {len(result['documents'])}")
        print(f"  Errors: {len(result['errors'])}")
        if result['documents']:
            first_doc = result['documents'][0]
            print(f"  First object: {first_doc['name']} ({first_doc['role']})")
            if 'documentation' in first_doc:
                print(f"  Has documentation: ✓")
            else:
                print(f"  Has documentation: ✗")
    except Exception as e:
        print(f"✗ ERROR: {e}")
    
    print()
    
    # Test 2: Explore with custom filters
    print("=== Test 2: Explore with filters ===")
    try:
        filters = Filters(
            domain="py",
            match_mode=interfaces.MatchMode.Fuzzy,
            fuzzy_threshold=60
        )
        result = await functions.explore(
            source, 
            "Data", 
            filters=filters,
            max_objects=3,
            include_documentation=False
        )
        print(f"✓ SUCCESS: Found {result['search_metadata']['object_count']} objects")
        print(f"  Applied filters: {result['search_metadata']['filters']}")
        print(f"  Documents: {len(result['documents'])}")
        print(f"  Errors: {len(result['errors'])}")
        if result['documents']:
            for i, doc in enumerate(result['documents']):
                fuzzy_info = f" (score: {doc['fuzzy_score']})" if 'fuzzy_score' in doc else ""
                print(f"  Object {i+1}: {doc['name']}{fuzzy_info}")
    except Exception as e:
        print(f"✗ ERROR: {e}")
    
    print()
    
    # Test 3: Explore with no results
    print("=== Test 3: Explore with no matches ===")
    try:
        result = await functions.explore(source, "NonExistentObject")
        print(f"✓ SUCCESS: Found {result['search_metadata']['object_count']} objects")
        print(f"  Documents: {len(result['documents'])}")
        print(f"  Errors: {len(result['errors'])}")
    except Exception as e:
        print(f"✗ ERROR: {e}")
    
    print()
    
    # Test 4: Test JSON serialization
    print("=== Test 4: JSON serialization ===")
    try:
        result = await functions.explore(source, "DataObj", max_objects=1)
        json_str = json.dumps(result, indent=2)
        print(f"✓ SUCCESS: Result is JSON serializable")
        print(f"  JSON length: {len(json_str)} characters")
    except Exception as e:
        print(f"✗ ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_explore_function())