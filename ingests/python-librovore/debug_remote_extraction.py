#!/usr/bin/env python3

import sys
import asyncio
sys.path.insert(0, 'sources')

async def debug_remote_extraction():
    """Debug remote site extraction step by step"""
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
        
        source = 'https://docs.python.org/3/'
        query = 'asyncio'
        
        print(f"=== Debugging {source} ===")
        
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
        candidate_objects = [result.object for result in search_results[:3]]
        
        print(f"Candidates found: {len(candidate_objects)}")
        for i, obj in enumerate(candidate_objects):
            print(f"  {i+1}: {obj['name']} (domain: {obj['domain']}, role: {obj['role']})")
        
        if not candidate_objects:
            return
            
        # Test extraction step by step
        from sphinxmcps.processors.sphinx.main import _extract_object_documentation
        from sphinxmcps.processors.sphinx import urls as _urls
        
        base_url = _urls.normalize_base_url(source)
        
        print(f"\n=== Testing individual extractions ===")
        for i, obj in enumerate(candidate_objects):
            print(f"\nTesting object {i+1}: {obj['name']}")
            try:
                result = await _extract_object_documentation(
                    base_url, obj, include_snippets=True
                )
                if result is None:
                    print("  Result: None (failed)")
                else:
                    print(f"  Result: Success - {result['object_name']}")
                    print(f"    Domain: {result.get('domain', 'MISSING')}")
                    print(f"    Score: {result.get('relevance_score', 'MISSING')}")
            except Exception as e:
                print(f"  Exception: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n=== Testing gather_async approach ===")
        tasks = [
            _extract_object_documentation(base_url, obj, True)
            for obj in candidate_objects
        ]
        candidate_results = await __.asyncf.gather_async(*tasks, return_exceptions=True)
        
        print(f"Gather results: {len(candidate_results)}")
        successful_results = []
        for i, result in enumerate(candidate_results):
            print(f"  Result {i}: type={type(result)}")
            if hasattr(__, 'generics') and __.generics.is_value(result):
                if result.value is not None:
                    successful_results.append(result.value)
                    print(f"    Success: {result.value['object_name']}")
                else:
                    print(f"    Value is None")
            else:
                print(f"    Not a successful result")
                
        print(f"\nFinal successful results: {len(successful_results)}")

if __name__ == '__main__':
    asyncio.run(debug_remote_extraction())