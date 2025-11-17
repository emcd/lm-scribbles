#!/usr/bin/env python3

import sys
import asyncio
sys.path.insert(0, 'sources')

async def debug_doc_extraction():
    """Debug what happens in documentation extraction"""
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
        
        # Step 1: Get processor and search results
        processor = await functions._determine_processor_optimal(source)
        filtered_objects = await processor.extract_filtered_inventory(
            source, 
            filters={},
            details=interfaces.InventoryQueryDetails.Name
        )
        search_results = search.filter_by_name(
            filtered_objects, query,
            match_mode=interfaces.MatchMode.Fuzzy,
            fuzzy_threshold=50
        )
        candidate_objects = [result.object for result in search_results]
        
        print(f"Found {len(candidate_objects)} candidate objects")
        if candidate_objects:
            print("First candidate:")
            print(f"  {candidate_objects[0]}")
        
        # Step 2: Try to extract documentation
        if candidate_objects:
            try:
                raw_results = await processor.extract_documentation_for_objects(
                    source, candidate_objects, include_snippets=True
                )
                print(f"\nDocumentation extraction results: {len(raw_results)}")
                for i, result in enumerate(raw_results):
                    print(f"  Result {i+1}: {result}")
            except Exception as e:
                print(f"\nDocumentation extraction failed: {e}")
                import traceback
                traceback.print_exc()
        
        # Step 3: Also try with a simpler object that might work
        print("\n" + "="*50)
        print("Trying with a different object...")
        
        # Find an object with a normal URI (not ending in #$)
        normal_objects = [obj for obj in filtered_objects if not obj['uri'].endswith('#$')]
        if normal_objects:
            print(f"Found {len(normal_objects)} objects with normal URIs")
            test_obj = normal_objects[0]
            print(f"Testing with: {test_obj}")
            
            try:
                raw_results = await processor.extract_documentation_for_objects(
                    source, [test_obj], include_snippets=True
                )
                print(f"Results: {len(raw_results)}")
                for result in raw_results:
                    print(f"  {result}")
            except Exception as e:
                print(f"Failed: {e}")
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(debug_doc_extraction())