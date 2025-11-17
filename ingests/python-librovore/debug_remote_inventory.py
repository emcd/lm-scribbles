#!/usr/bin/env python3

import sys
import asyncio
sys.path.insert(0, 'sources')

async def debug_remote_inventory():
    """Debug remote inventory structure vs local"""
    from sphinxmcps import functions
    from sphinxmcps import xtnsmgr
    from sphinxmcps.cli import _prepare
    from sphinxmcps import interfaces
    from sphinxmcps import search
    import contextlib
    
    async with contextlib.AsyncExitStack() as exits:
        auxdata = await _prepare(environment=True, exits=exits, logfile=None)
        await xtnsmgr.register_processors(auxdata)
        
        sources = [
            (".auxiliary/artifacts/sphinx-html", "local"),
            ("https://docs.python.org/3/", "Python docs"),
            ("https://flask.palletsprojects.com/en/stable/", "Flask docs")
        ]
        
        for source, name in sources:
            print(f"\n=== Debugging {name} ===")
            try:
                processor = await functions._determine_processor_optimal(source)
                filtered_objects = await processor.extract_filtered_inventory(
                    source, 
                    filters={},
                    details=interfaces.InventoryQueryDetails.Name
                )
                
                print(f"Total objects: {len(filtered_objects)}")
                if filtered_objects:
                    print(f"First object keys: {list(filtered_objects[0].keys())}")
                    print(f"Sample object: {filtered_objects[0]}")
                    
                    # Check domain field distribution
                    with_domain = [obj for obj in filtered_objects if 'domain' in obj and obj['domain']]
                    empty_domain = [obj for obj in filtered_objects if 'domain' in obj and not obj['domain']]
                    no_domain = [obj for obj in filtered_objects if 'domain' not in obj]
                    
                    print(f"Objects with domain: {len(with_domain)}")
                    print(f"Objects with empty domain: {len(empty_domain)}")  
                    print(f"Objects without domain key: {len(no_domain)}")
                    
                    if with_domain:
                        domains = set(obj['domain'] for obj in with_domain)
                        print(f"Domain values: {domains}")
                    
                    # Test search filtering
                    query = "flask" if "flask" in source else "asyncio" if "python" in source else "ProbeResponse"
                    search_results = search.filter_by_name(
                        filtered_objects, query,
                        match_mode=interfaces.MatchMode.Fuzzy,
                        fuzzy_threshold=50
                    )
                    print(f"Search results for '{query}': {len(search_results)}")
                    if search_results:
                        print(f"First result: {search_results[0].object}")
                        
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(debug_remote_inventory())