#!/usr/bin/env python3

import sys
import asyncio
sys.path.insert(0, 'sources')

async def debug_extraction_filtering():
    """Debug the extract_documentation_for_objects filtering logic"""
    from sphinxmcps import functions
    from sphinxmcps import xtnsmgr
    from sphinxmcps.cli import _prepare
    from sphinxmcps import search
    from sphinxmcps import interfaces
    from sphinxmcps import __
    import contextlib
    
    async with contextlib.AsyncExitStack() as exits:
        auxdata = await _prepare(environment=True, exits=exits, logfile=None)
        await xtnsmgr.register_processors(auxdata)
        
        source = '.auxiliary/artifacts/sphinx-html'
        query = 'ProbeResponse'
        
        # Get processor and candidate objects
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
        
        print(f"Testing with {len(candidate_objects)} candidate objects")
        if not candidate_objects:
            print("No candidates found!")
            return
            
        print(f"First candidate: {candidate_objects[0]}")
        
        # Now debug the extract_documentation_for_objects method step by step
        print("\n=== Debugging extract_documentation_for_objects ===")
        
        # Import the internal function
        from sphinxmcps.processors.sphinx.main import _extract_object_documentation
        from sphinxmcps.processors.sphinx import urls as _urls
        
        base_url = _urls.normalize_base_url(source)
        
        # Test the individual extraction function directly
        print("Testing _extract_object_documentation directly...")
        result = await _extract_object_documentation(
            base_url, candidate_objects[0], include_snippets=True
        )
        print(f"Direct result: {result}")
        print(f"Result type: {type(result)}")
        print(f"Result is None: {result is None}")
        
        # Test the gather_async approach
        print("\nTesting gather_async approach...")
        tasks = [
            _extract_object_documentation(base_url, obj, True)
            for obj in candidate_objects
        ]
        candidate_results = await __.asyncf.gather_async(*tasks, return_exceptions=True)
        print(f"Gather results count: {len(candidate_results)}")
        
        for i, result in enumerate(candidate_results):
            print(f"  Result {i}: {result}")
            print(f"    Type: {type(result)}")
            print(f"    Is value: {__.generics.is_value(result) if hasattr(__, 'generics') else 'no generics'}")
            if hasattr(__, 'generics') and __.generics.is_value(result):
                print(f"    Value: {result.value}")
                print(f"    Value is not None: {result.value is not None}")
        
        # Test the final filtering
        print("\nTesting final filtering...")
        if hasattr(__, 'generics'):
            filtered_results = [
                result.value for result in candidate_results
                if __.generics.is_value(result) and result.value is not None
            ]
            print(f"Filtered results count: {len(filtered_results)}")
            for i, result in enumerate(filtered_results):
                print(f"  Filtered result {i}: {result}")

if __name__ == '__main__':
    asyncio.run(debug_extraction_filtering())