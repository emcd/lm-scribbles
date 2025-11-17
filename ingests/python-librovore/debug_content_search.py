#!/usr/bin/env python3

import sys
import asyncio
sys.path.insert(0, 'sources')

async def debug_content_search():
    """Debug why query_content returns no results"""
    from sphinxmcps import functions
    from sphinxmcps import xtnsmgr
    from sphinxmcps.cli import _prepare
    from sphinxmcps import search
    from sphinxmcps import interfaces
    import contextlib
    
    async with contextlib.AsyncExitStack() as exits:
        auxdata = await _prepare(environment=True, exits=exits, logfile=None)
        await xtnsmgr.register_processors(auxdata)
        
        source = '.auxiliary/artifacts/sphinx-html'
        query = 'ProbeResponse'
        
        # Step 1: Get processor
        processor = await functions._determine_processor_optimal(source)
        print(f"Processor: {processor.name}")
        
        # Step 2: Get filtered inventory
        filtered_objects = await processor.extract_filtered_inventory(
            source, 
            filters={},
            details=interfaces.InventoryQueryDetails.Name
        )
        print(f"Total filtered objects: {len(filtered_objects)}")
        
        # Step 3: Show first few objects to see their structure
        print("\nFirst 3 objects:")
        for i, obj in enumerate(filtered_objects[:3]):
            print(f"  {i+1}: {obj}")
        
        # Step 4: Look for objects that contain "ProbeResponse"
        matching_objects = [obj for obj in filtered_objects if 'ProbeResponse' in str(obj)]
        print(f"\nObjects containing 'ProbeResponse': {len(matching_objects)}")
        for obj in matching_objects:
            print(f"  - {obj}")
        
        # Step 5: Try the search function
        search_results = search.filter_by_name(
            filtered_objects, query,
            match_mode=interfaces.MatchMode.Fuzzy,
            fuzzy_threshold=50
        )
        print(f"\nSearch results for '{query}': {len(search_results)}")
        for result in search_results[:3]:
            print(f"  - Score: {result.score}, Object: {result.object}")
        
        # Step 6: Try with lower fuzzy threshold
        search_results_low = search.filter_by_name(
            filtered_objects, query,
            match_mode=interfaces.MatchMode.Fuzzy,
            fuzzy_threshold=20
        )
        print(f"\nSearch results with lower threshold (20): {len(search_results_low)}")
        for result in search_results_low[:3]:
            print(f"  - Score: {result.score}, Object: {result.object}")
        
        # Step 7: Try exact match
        search_results_exact = search.filter_by_name(
            filtered_objects, query,
            match_mode=interfaces.MatchMode.Exact,
            fuzzy_threshold=50
        )
        print(f"\nExact search results: {len(search_results_exact)}")

if __name__ == '__main__':
    asyncio.run(debug_content_search())